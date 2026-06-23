# CLI-first Inspection

## Level

Beginner to intermediate, with expert tracing prompts.

## Audience

CAE engineers, Python developers, AI-agent builders, and instructors beginning the CaeReflex curriculum.

## Learning objectives

By the end, you can:

1. run a complete CaeReflex inspection from the command line;
2. identify the purpose of full case JSON, agent context JSON, and Markdown reports;
3. find inspection warnings and limitations; and
4. write a safe summary without claiming validation or certification.

## Files used

- `examples/openfoam_cavity_minimal`
- [Quickstart](../user-guide/quickstart.md)
- [CLI Reference](../reference/cli.md)

## Walkthrough

From the repository root:

```bash
caereflex examples list
caereflex examples run openfoam_cavity_minimal
caereflex inspect examples/openfoam_cavity_minimal \
  --out caereflex.json \
  --agent-context agent_context.json \
  --report case_report.md
```

Inspect the outputs:

```bash
python -m json.tool caereflex.json | head
python -m json.tool agent_context.json | head
sed -n '1,120p' case_report.md
```

## What to observe

- `caereflex.json` is the full structured record.
- `agent_context.json` is the compact LLM-oriented context.
- `case_report.md` is a human-readable report.
- Warnings and safe-use statements are part of the learning output, not noise to ignore.

## Beginner exercise

Find the case identifier, detected formats, detected tools, and at least one warning or limitation.

## Practitioner exercise

Write a five-sentence case summary that separates detected evidence from what a qualified engineer still needs to review.

## Expert extension

Trace the workflow through the architecture:

1. CLI command in `caereflex/cli/main.py`.
2. Service orchestration in `caereflex/services.py`.
3. OpenFOAM adapter behavior in `caereflex/adapters/openfoam.py`.
4. Export behavior in `caereflex/exporters.py`.
5. Domain records in `caereflex/core/models.py`.

## Assessment checklist

- [ ] Commands ran successfully.
- [ ] The learner can explain each generated file.
- [ ] The learner surfaced at least one limitation.
- [ ] The summary avoids claims of correctness, convergence, mesh adequacy, certification, or safety.
