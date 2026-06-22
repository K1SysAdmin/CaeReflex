from caereflex.adapters.gmsh import GmshAdapter

def test_gmsh_geo():
    r = GmshAdapter().inspect('examples/gmsh_minimal/t1.geo')
    assert r.case and '.geo' in r.case.detected_formats
