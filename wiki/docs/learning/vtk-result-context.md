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
