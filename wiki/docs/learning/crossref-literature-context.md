# CrossRef Literature Context

## Level

Beginner to advanced.

## Audience

Research engineers, students, technical writers, and agent developers adding literature metadata to simulation context.

## Learning objectives

By the end, you can:

1. attach deterministic mocked CrossRef metadata to a case;
2. export BibTeX references;
3. explain metadata-only limitations; and
4. prevent agents from claiming full-paper review or validation from CrossRef records.

## Files used

- `examples/crossref_context/sample_case.json`
- `examples/crossref_context/mock_crossref_response.json`
- [Architecture: CrossRef](../architecture/crossref.md)

## Walkthrough

```bash
caereflex crossref attach examples/crossref_context/sample_case.json \
  --mock-response examples/crossref_context/mock_crossref_response.json \
  --out caereflex.with_literature.json
caereflex export bibtex caereflex.with_literature.json --out references.bib
```

Review the outputs:

```bash
python -m json.tool caereflex.with_literature.json | head -120
sed -n '1,120p' references.bib
```

## What to observe

- The mock response keeps the exercise deterministic and offline.
- CrossRef records are bibliographic metadata and available abstracts when provided.
- Metadata can guide review, but it does not validate the simulation or prove that full papers were read.

## Expected output and interpretation

A representative enriched case using `examples/crossref_context/mock_crossref_response.json` should contain deterministic literature metadata:

```json
{
  "case_id": "case_sample_crossref",
  "literature_evidence": [
    {
      "doi": "10.0000/example.cavity.1",
      "title": "A benchmark study of incompressible lid-driven cavity flow",
      "evidence_status": "abstract_available",
      "trace": {"source_kind": "external_metadata", "adapter": "crossref"}
    },
    {
      "doi": "10.0000/example.openfoam.2",
      "title": "Finite volume methods for cavity flow examples",
      "evidence_status": "metadata_only"
    }
  ],
  "literature_context": {
    "records_used": ["10.0000/example.cavity.1", "10.0000/example.openfoam.2"],
    "summary": "CrossRef literature context generated from 2 metadata record(s); 1 record(s) included available abstracts."
  }
}
```

A representative BibTeX export should contain entries keyed from the deterministic fixture DOIs:

```bibtex
@article{ref1,
  title = {A benchmark study of incompressible lid-driven cavity flow},
  doi = {10.0000/example.cavity.1}
}
```

Interpret the output as follows:

- Extracted evidence: DOI, title, year, author, publisher metadata, and any provided abstract come from the mocked CrossRef response file.
- Inferred context: relevance scores, generated queries, and the summary are CaeReflex context-building outputs for review prioritization.
- Warnings: `literature_context.limitations` and `do_not_claim` are mandatory guardrails, especially for `metadata_only` records.
- Provenance: `crossref_attached` and each record trace identify CrossRef as external metadata, not a local simulation source.
- Unsafe claims to avoid: do not claim that CaeReflex read full papers, that metadata validates the simulation, that the cited work proves this case is correct, or that bibliography export is peer review.

## Beginner exercise

Find one title, DOI, or bibliographic field in the enriched case.

## Practitioner exercise

Write a short literature-context paragraph that says what metadata was attached and what must not be concluded from it.

## Expert extension

Inspect the CrossRef architecture and answer:

1. How does CaeReflex distinguish metadata-only records from abstract-available records?
2. Why should live network calls be optional in tests and teaching?
3. What language should an agent use when citing CrossRef metadata?

## Assessment checklist

- [ ] The learner used the mock CrossRef response.
- [ ] The learner exported BibTeX.
- [ ] The learner avoided saying CaeReflex read full papers or validated the simulation.
