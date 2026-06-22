# Install

CaeReflex is a Python 3.10+ package built with Hatchling.

```bash
pip install -e .
pip install -e ".[server]"
pip install -e ".[mesh]"
pip install -e ".[vtk]"
pip install -e ".[gmsh]"
pip install -e ".[all,dev]"
```

Core dependencies are Pydantic, Typer, Rich, HTTPX, PyYAML, and BibTeX parser support. Optional extras add FastAPI/Uvicorn, meshio/NumPy, PyVista/VTK, Gmsh, and pytest.
