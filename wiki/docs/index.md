# CaeReflex Wiki

CaeReflex is a Python package that turns Gmsh, OpenFOAM, VTK/ParaView-compatible artefacts, and optional CrossRef metadata into structured, provenance-aware `ReflexCase` records for humans and agents.

!!! warning "Boundary of use"
    CaeReflex is an inspection and documentation aid. It does not run solvers, validate simulations, prove convergence, certify engineering results, assess mesh adequacy, or establish design safety.

## Project spine

```text
simulation artefact
  -> caereflex.services.inspect_path()
  -> adapter detection
  -> GmshAdapter | OpenFOAMAdapter | VTKAdapter
  -> ReflexCase
  -> JSON | agent context | Markdown | BibTeX | REST | CLI
```

## Current release facts

| Fact | Value |
| --- | --- |
| Package version | `1.0.0` |
| ReflexCase schema version | `1.0` |
| CLI command | `caereflex` |
| Primary model | `caereflex.core.models.ReflexCase` |
| Service spine | `caereflex.services` |
| REST app factory | `caereflex.server.app.create_app` |

## Supported inspection paths

- Gmsh `.geo` files in core mode, plus `.msh` and CAD-like geometry fingerprinting.
- OpenFOAM-like case folders through read-only dictionary/text inspection.
- VTK-family files with legacy `.vtk` parsing and safe fingerprint fallback for XML-family files.
- CrossRef metadata and abstracts when explicitly requested.

## Start here

- [Quickstart](user-guide/quickstart.md)
- [Architecture](architecture/index.md)
- [Release controls](developer-guide/release-controls.md)
- [Release 1.0.0](releases/1.0.0.md)
