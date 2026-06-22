# Adapters

All adapters implement `BaseAdapter.inspect(path) -> AdapterResult`.

| Adapter | Inputs | Core behavior |
| --- | --- | --- |
| `GmshAdapter` | `.geo`, `.msh`, `.step`, `.stp`, `.iges`, `.igs` | Parses `.geo`, fingerprints mesh/geometry artefacts, records physical groups as boundary-condition-like records. |
| `OpenFOAMAdapter` | OpenFOAM-like folders | Reads expected dictionaries, initial fields, boundary files, limited logs/post-processing, and extracts solver/settings/fields/boundaries. |
| `VTKAdapter` | `.vtk`, `.vtu`, `.vtp`, `.vti`, `.vtr`, `.vts` | Parses tiny legacy `.vtk` files for dataset/points/cells/scalars/vectors; fingerprints other VTK-family files. |

Adapters must not write reports or REST responses directly. They return structured `AdapterResult` records.
