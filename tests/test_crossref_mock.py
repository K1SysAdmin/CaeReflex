from caereflex.services import load_case, attach_crossref

def test_crossref_mock():
    c = attach_crossref('examples/crossref_context/sample_case.json', mock_response='examples/crossref_context/mock_crossref_response.json', limit=5)
    assert len(c.literature_evidence) == 2
    assert c.literature_context.summary
