# REST API architecture

`caereflex.server.app.create_app` builds the FastAPI application.

Endpoints include:

- `GET /health`
- `GET /version`
- `GET /openapi.yaml`
- `POST /cases/import`
- `GET /cases`
- `GET /cases/{case_id}`
- `GET /cases/{case_id}/summary`
- `GET /cases/{case_id}/agent-context`
- `GET /cases/{case_id}/literature`
- `GET /cases/{case_id}/inspection-flags`
- `POST /cases/{case_id}/crossref/search`
- `POST /cases/{case_id}/crossref/attach`
- `POST /cases/{case_id}/export/json`
- `POST /cases/{case_id}/export/markdown`
- `POST /cases/{case_id}/export/bibtex`

External host mode requires an API key and constrains resolved paths to the configured workspace.
