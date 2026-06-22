from __future__ import annotations
from pathlib import Path
import json, re, time
from typing import Any
import httpx
from caereflex.core.models import ReflexCase, LiteratureEvidenceRecord, LiteratureContext, EvidenceStatus, TraceInfo, SourceKind, InspectionFlag, Severity, ProvenanceRecord

CROSSREF_URL = "https://api.crossref.org/works"


def generate_queries(case: ReflexCase, user_query: str | None = None, include_case_tags: bool = True) -> list[str]:
    queries: list[str] = []
    if user_query:
        queries.append(user_query)
    if include_case_tags:
        parts = [case.case_name, case.case_type.value if hasattr(case.case_type, 'value') else str(case.case_type)]
        parts += [str(x) for x in case.physics_tags[:5]]
        if case.detected_tools:
            parts += [str(x) for x in case.detected_tools]
        q = " ".join([p for p in parts if p and p != 'unknown']).strip()
        if q:
            queries.append(q)
    return list(dict.fromkeys(queries or [case.case_name]))


def load_mock_response(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def search_crossref(case: ReflexCase, query: str | None = None, limit: int = 10, mailto: str | None = None,
                    mock_response: str | Path | None = None, include_case_tags: bool = True,
                    timeout: float = 20.0) -> tuple[list[LiteratureEvidenceRecord], LiteratureContext]:
    queries = generate_queries(case, query, include_case_tags=include_case_tags)
    records: list[LiteratureEvidenceRecord] = []
    if mock_response:
        payload = load_mock_response(mock_response)
        used_query = queries[0] if queries else query or case.case_name
        records.extend(parse_crossref_items(payload, used_query, limit=limit))
    else:
        headers = {"User-Agent": "CaeReflex/1.0.0 (mailto:%s)" % mailto} if mailto else {"User-Agent": "CaeReflex/1.0.0"}
        for q in queries[:2]:
            params = {"query": q, "rows": limit}
            if mailto:
                params["mailto"] = mailto
            try:
                resp = httpx.get(CROSSREF_URL, params=params, headers=headers, timeout=timeout)
                resp.raise_for_status()
                records.extend(parse_crossref_items(resp.json(), q, limit=limit))
                time.sleep(0.1)
            except Exception as e:
                case.inspection_flags.append(InspectionFlag(severity=Severity.warning, category="crossref_error", message=f"CrossRef request failed: {e}"))
    # de-duplicate by DOI/title
    seen = set(); uniq = []
    for r in records:
        key = (r.doi or r.title or '').lower()
        if key and key not in seen:
            seen.add(key); uniq.append(r)
    uniq = uniq[:limit]
    ctx = build_literature_context(queries, uniq)
    return uniq, ctx


def parse_crossref_items(payload: dict[str, Any], query: str, limit: int = 10) -> list[LiteratureEvidenceRecord]:
    items = payload.get('message', {}).get('items', []) if isinstance(payload, dict) else []
    out: list[LiteratureEvidenceRecord] = []
    for item in items[:limit]:
        title = first(item.get('title'))
        abstract_raw = item.get('abstract')
        abstract = clean_abstract(abstract_raw) if abstract_raw else None
        status = EvidenceStatus.abstract_available if abstract else EvidenceStatus.metadata_only
        authors = []
        for a in item.get('author', [])[:8]:
            given = a.get('given', '')
            family = a.get('family', '')
            name = " ".join([given, family]).strip()
            if name: authors.append(name)
        year = None
        for key in ['published-print','published-online','published','created','issued']:
            parts = item.get(key, {}).get('date-parts')
            if parts and parts[0]:
                try: year = int(parts[0][0]); break
                except Exception: pass
        out.append(LiteratureEvidenceRecord(
            doi=item.get('DOI'), title=title, authors=authors, year=year,
            container_title=first(item.get('container-title')), url=item.get('URL'), abstract=abstract,
            evidence_status=status, relevance_score=relevance_score(query, title or '', abstract or ''), query=query,
            metadata_subset={"type": item.get('type'), "publisher": item.get('publisher'), "is-referenced-by-count": item.get('is-referenced-by-count')},
            trace=TraceInfo(source_kind=SourceKind.external_metadata, adapter="crossref", notes=["CrossRef metadata; not a full-paper retrieval."]),
        ))
    return out


def first(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def clean_abstract(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def relevance_score(query: str, title: str, abstract: str) -> float:
    q_terms = {t.lower() for t in re.findall(r"[A-Za-z0-9]+", query) if len(t) > 2}
    hay = (title + " " + abstract).lower()
    if not q_terms: return 0.0
    hits = sum(1 for t in q_terms if t in hay)
    return round(hits / len(q_terms), 3)


def build_literature_context(queries: list[str], records: list[LiteratureEvidenceRecord]) -> LiteratureContext:
    used = [r.doi or r.title or "record" for r in records]
    abstract_count = sum(1 for r in records if r.evidence_status == EvidenceStatus.abstract_available or r.evidence_status == 'abstract_available')
    summary = f"CrossRef literature context generated from {len(records)} metadata record(s); {abstract_count} record(s) included available abstracts."
    limitations = [
        "CrossRef metadata does not validate the simulation.",
        "Metadata-only records were not read as full papers.",
        "Coverage depends on metadata deposited with CrossRef.",
    ]
    return LiteratureContext(queries=queries, records_used=used, summary=summary, limitations=limitations)


def attach_crossref(case: ReflexCase, **kwargs: Any) -> ReflexCase:
    records, context = search_crossref(case, **kwargs)
    case.literature_evidence = records
    case.literature_context = context
    case.provenance.append(ProvenanceRecord(event="crossref_attached", details={"records": len(records), "queries": context.queries}))
    return case
