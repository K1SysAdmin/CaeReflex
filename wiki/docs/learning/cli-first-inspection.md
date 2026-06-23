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

## Expected output and interpretation

A representative `agent_context.json` from `examples/openfoam_cavity_minimal` should contain stable, file-derived evidence like this:

```json
{
  "case_name": "openfoam_cavity_minimal",
  "case_type": "openfoam",
  "detected_formats": ["OpenFOAM case folder"],
  "detected_tools": ["OpenFOAM"],
  "source_files": [
    {"relative_path": "system/controlDict", "hash_status": "complete"},
    {"relative_path": "0/U", "hash_status": "complete"}
  ],
  "result_fields": [
    {"name": "p", "association": "volume", "trace": {"source_kind": "extracted", "source_files": ["0/p"]}},
    {"name": "U", "association": "volume", "trace": {"source_kind": "extracted", "source_files": ["0/U"]}}
  ]
}
```

A representative Markdown report should start with safe-use framing:

```markdown
# CaeReflex Report — openfoam_cavity_minimal
This report was generated from metadata extracted or inferred by CaeReflex.
It is not an engineering validation report, certification, safety approval, or convergence proof.
```

Interpret the output as follows:

- Extracted evidence: `source_files`, `detected_formats`, `detected_tools`, and `result_fields[*].trace.source_files` are direct observations from files under `examples/openfoam_cavity_minimal`.
- Inferred context: `case_type: "openfoam"` and the human-readable summary classify the folder from its layout and known dictionary names; treat them as adapter interpretation, not solver execution.
- Warnings: `inspection_warnings` or `inspection_flags` must be preserved verbatim when present. An empty list only means this inspection did not emit a warning; it is not proof that the case is complete.
- Provenance: `source_references` or full-case `provenance` events identify which adapter actions produced the context.
- Unsafe claims to avoid: do not say the simulation converged, the mesh is adequate, the boundary conditions are correct, the result is certified, or the design is safe.

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
