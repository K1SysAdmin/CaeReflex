from caereflex.services import inspect_path, export_case

def test_agent_context_no_absolute_paths(tmp_path):
    c = inspect_path('examples/openfoam_cavity_minimal', adapter='openfoam')
    out = tmp_path/'ctx.json'
    export_case(c, 'agent-context', out)
    text = out.read_text()
    assert '/mnt/data' not in text and '/home/' not in text
