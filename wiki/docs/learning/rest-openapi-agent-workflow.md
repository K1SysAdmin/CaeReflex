# REST/OpenAPI Agent Workflow

## Level

Intermediate to expert.

## Audience

Full-stack developers, AI-agent engineers, platform teams, and instructors teaching tool-calling workflows.

## Learning objectives

By the end, you can:

1. start the CaeReflex REST server in a bounded workspace;
2. inspect health and OpenAPI endpoints;
3. import a case through the API;
4. retrieve agent context and inspection flags; and
5. design safe tool instructions for Custom GPT, Claude-style, or internal agents.

## Files used

- [Architecture: REST API](../architecture/rest-api.md)
- [Reference: OpenAPI](../reference/openapi.md)
- `openapi/openapi.yaml`
- `examples/agent_workflow/`

## Walkthrough

Start the server from the repository root:

```bash
caereflex serve --host 127.0.0.1 --port 8765 --workspace .
```

In another terminal:

```bash
curl http://127.0.0.1:8765/health
curl http://127.0.0.1:8765/openapi.yaml
curl -X POST "http://127.0.0.1:8765/cases/import" \
  -H "Content-Type: application/json" \
  -d '{"path":"examples/openfoam_cavity_minimal","adapter":"auto","attach_crossref":false,"return_agent_context":true}'
```

Use the returned `case_id`:

```bash
curl "http://127.0.0.1:8765/cases/CASE_ID/agent-context"
curl "http://127.0.0.1:8765/cases/CASE_ID/inspection-flags"
```

## What to observe

- The OpenAPI schema describes the tool surface for action-capable agents.
- Case paths should be workspace-relative.
- CrossRef should be requested explicitly, not silently.
- Agent answers must preserve inspection warnings and safe-use policy.

## Expected output and interpretation

A representative health response is intentionally small:

```json
{"status": "ok", "service": "caereflex"}
```

A representative import response for `examples/openfoam_cavity_minimal` should include the stored case identifier and optional agent context:

```json
{
  "status": "success",
  "case_id": "case_6c5707a83ec1",
  "summary": "OpenFOAM case inspected. 8 files were considered.",
  "warnings": [],
  "provenance_summary": ["openfoam_inspection_started"],
  "next_recommended_actions": ["get_agent_context", "export_case_report"],
  "data": {
    "agent_context": {
      "case_type": "openfoam",
      "source_files": [{"relative_path": "system/controlDict", "hash_status": "complete"}],
      "do_not_claim": ["Do not claim simulation convergence unless explicit evidence is present."]
    }
  }
}
```

A representative inspection-flags response is:

```json
{"inspection_flags": []}
```

Interpret the output as follows:

- Extracted evidence: `source_files`, `detected_formats`, field records, and hashes in `data.agent_context` come from the workspace-relative example path.
- Inferred context: `summary`, `next_recommended_actions`, and case classification help sequence agent behavior; they are not engineering conclusions.
- Warnings: top-level `warnings` and `/inspection-flags` must be fetched and echoed before summarization. An empty list is only an absence of emitted flags for that run.
- Provenance: `provenance_summary` identifies adapter events that produced the stored case.
- Unsafe claims to avoid: agents must not claim validation, convergence, mesh adequacy, certification, design safety, unrestricted filesystem access, or CrossRef attachment unless the corresponding endpoint was explicitly called.

## Beginner exercise

Identify the health endpoint, OpenAPI endpoint, import endpoint, and agent-context endpoint.

## Practitioner exercise

Draft safe agent instructions that require health check, case import, agent context retrieval, and inspection flag review before summarization.

## Expert extension

Review API exposure risks:

1. What changes when binding outside localhost?
2. Why is an API key required for external exposure?
3. How should workspace boundaries shape agent tool descriptions?
4. What should an agent do if a user provides an absolute path?

## Assessment checklist

- [ ] The learner understands the REST workflow sequence.
- [ ] The learner can write a safe agent prompt or tool policy.
- [ ] The learner explains workspace and authentication risks.
