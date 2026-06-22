from pathlib import Path

def test_examples_presence():
    for name in ['gmsh_minimal','openfoam_cavity_minimal','vtk_minimal','crossref_context','agent_workflow']:
        assert Path('examples', name, 'README.md').exists()
