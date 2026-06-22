from caereflex.adapters.vtk import VTKAdapter

def test_vtk_minimal():
    r = VTKAdapter().inspect('examples/vtk_minimal/sample.vtk')
    assert r.case and '.vtk' in r.case.detected_formats
    assert r.case.result_fields
