# Security

Security-relevant behavior includes:

- REST external-host mode requires an API key.
- External REST paths are constrained to the configured workspace.
- Agent-context export guards against common absolute path disclosure patterns.
- CaeReflex performs read-only inspection of simulation artefacts; it does not execute OpenFOAM, Gmsh, or VTK solvers.
