# CrossRef Literature Context

## Level

Beginner to advanced.

## Audience

Research engineers, students, technical writers, and agent developers adding literature metadata to simulation context.

## Learning objectives

By the end, you can:

1. attach deterministic mocked CrossRef metadata to a case;
2. export BibTeX references;
3. explain metadata-only limitations; and
4. prevent agents from claiming full-paper review or validation from CrossRef records.

## Files used

- `examples/crossref_context/sample_case.json`
- `examples/crossref_context/mock_crossref_response.json`
- [Architecture: CrossRef](../architecture/crossref.md)

## Walkthrough

```bash
caereflex crossref attach examples/crossref_context/sample_case.json \
  --mock-response examples/crossref_context/mock_crossref_response.json \
  --out caereflex.with_literature.json
caereflex export bibtex caereflex.with_literature.json --out references.bib
```

Review the outputs:

```bash
python -m json.tool caereflex.with_literature.json | head -120
sed -n '1,120p' references.bib
```

## What to observe

- The mock response keeps the exercise deterministic and offline.
- CrossRef records are bibliographic metadata and available abstracts when provided.
- Metadata can guide review, but it does not validate the simulation or prove that full papers were read.

## Beginner exercise

Find one title, DOI, or bibliographic field in the enriched case.

## Practitioner exercise

Write a short literature-context paragraph that says what metadata was attached and what must not be concluded from it.

## Expert extension

Inspect the CrossRef architecture and answer:

1. How does CaeReflex distinguish metadata-only records from abstract-available records?
2. Why should live network calls be optional in tests and teaching?
3. What language should an agent use when citing CrossRef metadata?

## Assessment checklist

- [ ] The learner used the mock CrossRef response.
- [ ] The learner exported BibTeX.
- [ ] The learner avoided saying CaeReflex read full papers or validated the simulation.
