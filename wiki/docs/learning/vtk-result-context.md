# VTK Result Context

## Level

Intermediate, with beginner and expert options.

## Audience

Post-processing users, visualization engineers, data engineers, and developers handling optional scientific dependencies.

## Learning objectives

By the end, you can:

1. inspect a VTK-family result file;
2. describe result-field context safely;
3. explain why field presence is not correctness evidence; and
4. discuss optional dependency fallback behavior.

## Files used

- `examples/vtk_minimal/sample.vtk`
- [Architecture: Adapters](../architecture/adapters.md)

## Walkthrough

```bash
caereflex inspect-vtk examples/vtk_minimal/sample.vtk --out vtk_case.json
caereflex export agent-context vtk_case.json --out vtk_agent_context.json
```

Review the context:

```bash
python -m json.tool vtk_agent_context.json | head -100
```

## What to observe

- Result files may expose fields, metadata, or safe fingerprints.
- Rich VTK/PyVista behavior can depend on optional packages.
- Result context does not prove convergence, mesh adequacy, or physical correctness.

## Expected output and interpretation

A representative `vtk_agent_context.json` for `examples/vtk_minimal/sample.vtk` should show dataset and field context like this:

```json
{
  "case_name": "sample",
  "case_type": "vtk",
  "detected_formats": [".vtk"],
  "detected_tools": ["VTK/ParaView-compatible"],
  "assets": [
    {"asset_type": "result_file", "name": "sample.vtk", "metrics": {"dataset_type": "POLYDATA", "points": 4, "cells": null}}
  ],
  "result_fields": [
    {"name": "pressure", "association": "point", "field_type": "scalar", "components": 1},
    {"name": "velocity", "association": "point", "field_type": "vector", "components": 3}
  ]
}
```

Interpret the output as follows:

- Extracted evidence: the `.vtk` suffix, `POLYDATA` dataset type, point count, and point-data field names are read from `examples/vtk_minimal/sample.vtk`.
- Inferred context: `detected_tools: ["VTK/ParaView-compatible"]` indicates a compatible result format, not the actual solver or visualization workflow used.
- Warnings: optional-reader fallback warnings, if present, mean the context may be less rich and should be surfaced to the user.
- Provenance: the full JSON includes `vtk_inspection_started` and a trace pointing back to `sample.vtk`.
- Unsafe claims to avoid: do not claim convergence, interpolation quality, unit correctness, solver provenance, physical correctness, mesh adequacy, or validated results from field presence alone.

## Beginner exercise

Identify the inspected file and any result-context information present in the output.

## Practitioner exercise

Draft an agent response that describes the detected VTK evidence and explicitly names what is not proven.

## Expert extension

Study the VTK adapter and answer:

1. What happens when optional readers are unavailable?
2. Which behavior should remain available in the base install?
3. Which tests would protect fallback behavior?

## Assessment checklist

- [ ] The learner inspected the VTK example.
- [ ] The learner avoids treating fields as validation evidence.
- [ ] The learner can explain optional dependency implications.
