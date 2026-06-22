from caereflex.services import inspect_path, export_case

def test_exports(tmp_path):
    c = inspect_path('examples/openfoam_cavity_minimal', adapter='openfoam')
    ctx = tmp_path/'agent_context.json'; md = tmp_path/'report.md'; bib = tmp_path/'refs.bib'
    export_case(c, 'agent-context', ctx)
    export_case(c, 'markdown', md)
    export_case(c, 'bibtex', bib)
    assert ctx.exists() and md.exists() and bib.exists()
    assert '/mnt/data' not in ctx.read_text()
