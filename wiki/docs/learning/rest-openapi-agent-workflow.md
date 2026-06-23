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
