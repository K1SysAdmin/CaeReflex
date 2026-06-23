# Gmsh Geometry Inspection

## Level

Beginner to advanced.

## Audience

Geometry users, mesh-generation learners, and developers studying adapter behavior.

## Learning objectives

By the end, you can:

1. inspect a Gmsh `.geo` file;
2. describe what geometry evidence CaeReflex can extract;
3. avoid treating geometry inspection as mesh or design validation; and
4. connect adapter output to the ReflexCase model.

## Files used

- `examples/gmsh_minimal/t1.geo`
- [Architecture: Adapters](../architecture/adapters.md)
- [Developer Guide: Adding Adapters](../developer-guide/adding-adapters.md)

## Walkthrough

```bash
caereflex inspect-gmsh examples/gmsh_minimal/t1.geo --out gmsh_case.json
caereflex export markdown gmsh_case.json --out gmsh_report.md
```

Review the report:

```bash
sed -n '1,140p' gmsh_report.md
```

## What to observe

- The input is a geometry script, not a completed engineering validation package.
- CaeReflex can record file evidence, detected format, and adapter findings.
- Any downstream mesh adequacy or physical suitability claim requires independent engineering review.

## Beginner exercise

Identify the inspected source file, detected format, and generated output file.

## Practitioner exercise

Explain which facts came from the `.geo` file and which statements would be unsafe to infer.

## Expert extension

Read the Gmsh adapter and answer:

1. Which fields are extracted directly?
2. Which limitations should appear in the report or agent context?
3. How would optional Gmsh SDK support change inspection without breaking base imports?

## Assessment checklist

- [ ] The learner inspected the Gmsh example.
- [ ] The learner can describe geometry evidence without claiming mesh adequacy.
- [ ] The learner identifies where adapter responsibilities end.
