# Learning Projects

The CaeReflex learning projects are a guided curriculum for engineers, developers, and agent builders who need to turn CAE artefacts into structured, provenance-aware evidence without overstating what the software can prove.

!!! warning "Boundary of use"
    CaeReflex is an inspection and documentation aid. It does not run solvers, validate simulations, prove convergence, assess mesh adequacy, certify engineering results, or establish design safety.

## How to use this curriculum

Each project uses the same teaching pattern:

1. **Beginner path**: run a bounded workflow and observe the output.
2. **Practitioner path**: interpret the output, explain limitations, and prepare a safe summary.
3. **Expert path**: trace the implementation, critique the design, and propose safe extensions.

You can complete the projects in order, or choose a path from [Learning Paths](learning-paths.md).

## Project sequence

| Project | Main skill | Primary example | Best first audience |
| --- | --- | --- | --- |
| [CLI-first Inspection](cli-first-inspection.md) | Run a complete offline inspection | `examples/openfoam_cavity_minimal` | Everyone |
| [Gmsh Geometry Inspection](gmsh-geometry-inspection.md) | Inspect geometry evidence | `examples/gmsh_minimal/t1.geo` | Geometry and mesh users |
| [OpenFOAM Case Review](openfoam-case-review.md) | Review folder-based solver artefacts | `examples/openfoam_cavity_minimal` | CFD and CAE engineers |
| [VTK Result Context](vtk-result-context.md) | Inspect result-file context | `examples/vtk_minimal/sample.vtk` | Post-processing users |
| [CrossRef Literature Context](crossref-literature-context.md) | Attach deterministic literature metadata | `examples/crossref_context` | Research engineers |
| [REST/OpenAPI Agent Workflow](rest-openapi-agent-workflow.md) | Expose CaeReflex to tool-calling agents | `openapi/openapi.yaml` | Full-stack and AI-agent developers |
| [Adapter Extension Design](adapter-extension-design.md) | Design a safe new adapter | adapter and service docs | Contributors and maintainers |

## Shared references

- [Environment Setup](environment-setup.md)
- [Assessment Rubric](assessment-rubric.md)
- [Glossary](glossary.md)
- [Instructor Guide](instructor-guide.md)

## Completion standard

A learner is successful when they can:

- run the relevant workflow;
- identify generated artefacts and their intended audience;
- separate extracted evidence from assumptions;
- surface inspection warnings as review prompts;
- preserve provenance and safe-use language; and
- avoid claims that CaeReflex validates, certifies, proves convergence, or establishes safety.
