# CLI architecture

The console script is `caereflex = caereflex.cli.main:app`.

Commands:

- `version`
- `inspect`
- `inspect-gmsh`
- `inspect-openfoam`
- `inspect-vtk`
- `crossref search`
- `crossref attach`
- `export agent-context`
- `export markdown`
- `export bibtex`
- `serve`
- `examples list`
- `examples run`

The CLI delegates inspection, CrossRef, examples, and exports to `caereflex.services`.
