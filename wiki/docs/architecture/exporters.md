# Exporters

`caereflex.exporters` converts a `ReflexCase` into downstream formats:

- ReflexCase JSON
- agent-context JSON
- agent-context Markdown
- case-report Markdown
- BibTeX

The agent-context export separates extracted and inferred facts, includes a safe-use policy, includes do-not-claim rules, and guards against common absolute path disclosure patterns.
