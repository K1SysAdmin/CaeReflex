# Quickstart

Offline path:

```bash
caereflex examples list
caereflex examples run openfoam_cavity_minimal
caereflex inspect examples/openfoam_cavity_minimal --out caereflex.json
caereflex export agent-context caereflex.json --out agent_context.json
caereflex export markdown caereflex.json --out case_report.md
```

Mock CrossRef path:

```bash
caereflex crossref attach examples/crossref_context/sample_case.json \
  --mock-response examples/crossref_context/mock_crossref_response.json \
  --out caereflex.with_literature.json
caereflex export bibtex caereflex.with_literature.json --out references.bib
```
