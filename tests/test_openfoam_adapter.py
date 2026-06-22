from caereflex.adapters.openfoam import OpenFOAMAdapter

def test_openfoam_minimal():
    r = OpenFOAMAdapter().inspect('examples/openfoam_cavity_minimal')
    assert r.case and r.case.case_type == 'openfoam'
    assert r.case.source_files
