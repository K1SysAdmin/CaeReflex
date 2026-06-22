#!/usr/bin/env bash
set -euo pipefail
python -c "import caereflex; print(caereflex.__version__)"
python -m caereflex.cli.main version
python -m caereflex.cli.main examples list
python -m caereflex.cli.main examples run openfoam_cavity_minimal
python -m caereflex.cli.main inspect-openfoam examples/openfoam_cavity_minimal --out build/openfoam_case.json
python -m caereflex.cli.main inspect-gmsh examples/gmsh_minimal/t1.geo --out build/gmsh_case.json
python -m caereflex.cli.main inspect-vtk examples/vtk_minimal/sample.vtk --out build/vtk_case.json
python -m caereflex.cli.main export agent-context build/openfoam_case.json --out build/agent_context.json
python -m caereflex.cli.main export markdown build/openfoam_case.json --out build/case_report.md
python -m caereflex.cli.main crossref attach examples/crossref_context/sample_case.json --mock-response examples/crossref_context/mock_crossref_response.json --out build/case_with_literature.json --limit 5
python -m caereflex.cli.main export bibtex build/case_with_literature.json --out build/references.bib
pytest
