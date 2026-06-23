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

## Expected output and interpretation

A representative `gmsh_case.json` for `examples/gmsh_minimal/t1.geo` should include geometry-script evidence like this:

```json
{
  "case_name": "t1",
  "case_type": "gmsh",
  "detected_formats": [".geo"],
  "detected_tools": ["Gmsh"],
  "source_files": [
    {"relative_path": "t1.geo", "suffix": ".geo", "hash_status": "complete"}
  ],
  "assets": [
    {
      "asset_type": "geometry",
      "name": "t1.geo",
      "metrics": {"points_declared": 4, "lines_declared": 4, "surfaces_declared": 2, "physical_groups": 2}
    }
  ]
}
```

Interpret the output as follows:

- Extracted evidence: the `.geo` suffix, file hash status, declared points, lines, surfaces, and physical groups come from `examples/gmsh_minimal/t1.geo`.
- Inferred context: `case_type: "gmsh"`, `detected_tools: ["Gmsh"]`, and `asset_type: "geometry"` are adapter classifications based on the input file.
- Warnings: any warning about missing mesh-reader support or partial parsing should be treated as a review prompt, not hidden from learners.
- Provenance: a full case includes events such as `gmsh_inspection_started` with the inspected path.
- Unsafe claims to avoid: do not claim that a mesh was generated, mesh quality is acceptable, geometry is watertight, boundary groups are physically correct, or the design is validated.

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
