# OpenFOAM Case Review

## Level

Beginner to expert.

## Audience

CFD engineers, CAE reviewers, and developers working with folder-based simulation artefacts.

## Learning objectives

By the end, you can:

1. inspect an OpenFOAM-like case folder;
2. identify solver dictionaries, boundary-condition files, material files, and numerical settings when detected;
3. interpret inspection flags as review prompts; and
4. state what a qualified engineer still needs to verify.

## Files used

- `examples/openfoam_cavity_minimal`
- [Architecture: Adapters](../architecture/adapters.md)
- [Safe Use Policy](../user-guide/safe-use-policy.md)

## Walkthrough

```bash
caereflex inspect-openfoam examples/openfoam_cavity_minimal --out openfoam_case.json
caereflex export agent-context openfoam_case.json --out openfoam_agent_context.json
caereflex export markdown openfoam_case.json --out openfoam_report.md
```

Review the outputs:

```bash
python -m json.tool openfoam_agent_context.json | head -80
sed -n '1,160p' openfoam_report.md
```

## What to observe

- CaeReflex reads OpenFOAM-like text files; it does not run OpenFOAM.
- Dictionary and boundary-condition evidence can help structure review.
- Missing or partial evidence should be carried into the final summary.

## Beginner exercise

List three files from the case folder that CaeReflex inspected or referenced.

## Practitioner exercise

Write a review note with three sections: detected evidence, inspection limitations, and human follow-up checks.

## Expert extension

Inspect how the OpenFOAM adapter handles bounded scanning and safe text inspection. Propose one additional inspection flag that would improve review quality while staying read-only.

## Assessment checklist

- [ ] The learner distinguishes file inspection from solver execution.
- [ ] The learner explains at least one detected setting or source file.
- [ ] The learner lists follow-up checks without saying CaeReflex validated the simulation.
