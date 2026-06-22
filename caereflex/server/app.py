from __future__ import annotations
from pathlib import Path
from typing import Any
import json
import yaml
try:
    from fastapi import FastAPI, Header, HTTPException, Request
    from fastapi.responses import JSONResponse, PlainTextResponse
    from pydantic import BaseModel
except Exception:  # pragma: no cover
    FastAPI = None
from caereflex.version import __version__
from caereflex.core.config import CaeReflexConfig
from caereflex.core.validation import assert_safe_workspace_path
from caereflex.services import inspect_path, save_case_to_store, load_case_from_store, list_case_store, attach_crossref, save_case, export_case
from caereflex.exporters import agent_context_dict, case_to_dict

if FastAPI:
    class ImportRequest(BaseModel):
        path: str
        adapter: str = "auto"
        attach_crossref: bool = False
        return_agent_context: bool = True
        options: dict[str, Any] = {}
    class CrossRefRequest(BaseModel):
        query: str | None = None
        include_case_tags: bool = True
        limit: int = 10
        mailto: str | None = None
        mock_response: str | None = None
    class ExportRequest(BaseModel):
        out: str | None = None


def create_app(workspace: str | Path = '.', api_key: str | None = None, host: str = '127.0.0.1'):
    if FastAPI is None:
        raise RuntimeError("FastAPI is not installed. Install caereflex[server].")
    app = FastAPI(title="CaeReflex API", version=__version__, description="Safe REST/OpenAPI interface for CaeReflex ReflexCase workflows.")
    ws = Path(workspace).resolve()
    external = host not in {"127.0.0.1", "localhost"}

    def check_key(x_api_key: str | None):
        if external and (not api_key or x_api_key != api_key):
            raise HTTPException(status_code=401, detail="API key required outside localhost.")

    def resolve_path(p: str) -> Path:
        path = (ws / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
        if external:
            assert_safe_workspace_path(path, ws)
        return path

    @app.get('/health')
    def health(): return {"status": "success", "service": "caereflex", "version": __version__}

    @app.get('/version')
    def version(): return {"version": __version__}

    @app.get('/openapi.yaml', response_class=PlainTextResponse)
    def openapi_yaml(): return yaml.safe_dump(app.openapi(), sort_keys=False)

    @app.post('/cases/import')
    def import_case(req: ImportRequest, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key)
        try:
            p = resolve_path(req.path)
            case = inspect_path(p, adapter=req.adapter, attach_crossref=req.attach_crossref)
            save_case_to_store(case, ws)
            data = {"status": case.inspection.status, "case_id": case.case_id, "summary": case.agent_summary.summary, "warnings": [f.message for f in case.inspection_flags], "inspection_flags": [f.model_dump(mode='json') for f in case.inspection_flags], "provenance_summary": [p.event for p in case.provenance], "next_recommended_actions": ["get_agent_context", "export_case_report"]}
            if req.return_agent_context:
                data["data"] = {"agent_context": agent_context_dict(case)}
            return data
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get('/cases')
    def cases(x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); return {"status": "success", "cases": list_case_store(ws)}

    @app.get('/cases/{case_id}')
    def get_case(case_id: str, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); return case_to_dict(load_case_from_store(case_id, ws))

    @app.get('/cases/{case_id}/summary')
    def get_summary(case_id: str, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); return {"status": c.inspection.status, "case_id": c.case_id, "summary": c.agent_summary.summary, "detected_formats": c.detected_formats, "detected_tools": c.detected_tools}

    @app.get('/cases/{case_id}/agent-context')
    def get_agent_context(case_id: str, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); return agent_context_dict(load_case_from_store(case_id, ws))

    @app.get('/cases/{case_id}/literature')
    def get_literature(case_id: str, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); return {"literature_evidence": [r.model_dump(mode='json') for r in c.literature_evidence], "literature_context": c.literature_context.model_dump(mode='json')}

    @app.get('/cases/{case_id}/inspection-flags')
    def get_flags(case_id: str, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); return {"inspection_flags": [f.model_dump(mode='json') for f in c.inspection_flags]}

    @app.post('/cases/{case_id}/crossref/search')
    def crossref_search(case_id: str, req: CrossRefRequest, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key)
        from caereflex.services import search_crossref
        c = load_case_from_store(case_id, ws)
        records, ctx = search_crossref(c, query=req.query, include_case_tags=req.include_case_tags, limit=req.limit, mailto=req.mailto, mock_response=req.mock_response)
        return {"records": [r.model_dump(mode='json') for r in records], "literature_context": ctx.model_dump(mode='json')}

    @app.post('/cases/{case_id}/crossref/attach')
    def crossref_attach(case_id: str, req: CrossRefRequest, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); c = attach_crossref(c, query=req.query, include_case_tags=req.include_case_tags, limit=req.limit, mailto=req.mailto, mock_response=req.mock_response); save_case_to_store(c, ws); return case_to_dict(c)

    @app.post('/cases/{case_id}/export/json')
    def export_json(case_id: str, req: ExportRequest, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); return case_to_dict(c)

    @app.post('/cases/{case_id}/export/markdown')
    def export_markdown(case_id: str, req: ExportRequest, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); out = Path(req.out or f"{case_id}.md"); export_case(c, 'markdown', ws / out); return {"status": "success", "out": str(out)}

    @app.post('/cases/{case_id}/export/bibtex')
    def export_bibtex(case_id: str, req: ExportRequest, x_api_key: str | None = Header(default=None)):
        check_key(x_api_key); c = load_case_from_store(case_id, ws); out = Path(req.out or f"{case_id}.bib"); export_case(c, 'bibtex', ws / out); return {"status": "success", "out": str(out)}

    return app

app = create_app()

def generate_openapi_files(out_dir: str | Path = 'openapi') -> None:
    d = Path(out_dir); d.mkdir(parents=True, exist_ok=True)
    schema = app.openapi()
    (d / 'openapi.json').write_text(json.dumps(schema, indent=2), encoding='utf-8')
    (d / 'openapi.yaml').write_text(yaml.safe_dump(schema, sort_keys=False), encoding='utf-8')
