# Services layer

`caereflex.services` is the application spine.

Key responsibilities:

- `inspect_path`: inspect a path through explicit or auto-detected adapters.
- `detect_adapter`: map input paths to `gmsh`, `openfoam`, or `vtk`.
- `inspect_with_adapter`: call the selected adapter.
- `search_crossref` and `attach_crossref`: delegate literature metadata handling.
- `export_case`: route JSON, agent-context, Markdown, and BibTeX exports.
- Case-store helpers: save, load, and list `.caereflex/cases/case_*.json`.
- Example helpers: discover and run bundled examples.
