# crossref_context

Mock-first CrossRef example. Normal tests use `mock_crossref_response.json`; no live CrossRef call is required.

Run:

```bash
caereflex crossref attach examples/crossref_context/sample_case.json \
  --mock-response examples/crossref_context/mock_crossref_response.json \
  --out build/case_with_literature.json
```
