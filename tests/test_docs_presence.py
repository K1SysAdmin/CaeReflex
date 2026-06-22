from pathlib import Path

def test_docs_presence():
    root = Path('.')
    for p in ['README.md','INSTALL.md','QUICKSTART.md','LICENSE.md','ACADEMIC_USE.md','COMMERCIAL_LICENSE.md','NOTICE.md','THIRD_PARTY_NOTICES.md','CITATION.cff','SECURITY.md','CHANGELOG.md','docs/CLI.md','docs/REST_API.md','docs/AGENT_INTEGRATION.md','docs/REFLEXCASE_SCHEMA.md','docs/ADAPTERS.md','docs/CROSSREF.md','docs/EXAMPLES.md','docs/DEVELOPER_GUIDE.md','docs/LICENSING.md']:
        assert (root/p).exists(), p
