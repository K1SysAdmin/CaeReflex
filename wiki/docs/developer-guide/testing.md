# Testing

The existing test suite covers imports, models, hashing, adapters, exporters, security/path display behavior, mock CrossRef, CLI, server, docs presence, and examples presence.

For wiki changes, run:

```bash
python wiki/scripts/validate_wiki.py
python -m mkdocs build -f wiki/mkdocs.yml --strict
pytest tests/test_wiki.py
```
