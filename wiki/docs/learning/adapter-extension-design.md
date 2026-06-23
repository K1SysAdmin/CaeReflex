# Adapter Extension Design

## Level

Advanced to expert, with an accessible conceptual entry point.

## Audience

Python developers, engineering-software contributors, maintainers, and technical leads planning support for new CAE artefacts.

## Learning objectives

By the end, you can:

1. explain what a CaeReflex adapter owns;
2. design a read-only adapter workflow;
3. identify service, CLI, REST, exporter, docs, and test implications; and
4. preserve safety boundaries while extending evidence coverage.

## Files used

- [Architecture: Adapters](../architecture/adapters.md)
- [Architecture: Services Layer](../architecture/services-layer.md)
- [Developer Guide: Adding Adapters](../developer-guide/adding-adapters.md)
- [Developer Guide: Testing](../developer-guide/testing.md)

## Concept walkthrough

An adapter should inspect files and return structured evidence. It should not run solvers, execute scripts, mutate cases, or claim engineering correctness.

A safe adapter design should define:

1. supported file extensions or folder patterns;
2. scan limits and file-size behavior;
3. extracted facts;
4. inferred facts, if any;
5. inspection flags for partial or missing evidence;
6. provenance events;
7. tests for happy path, partial path, and safety limits; and
8. documentation and examples if the adapter is public.

## Beginner exercise

Choose a hypothetical artefact type and write three facts an adapter might safely extract from files.

## Practitioner exercise

Draft an adapter design brief with:

- input shape;
- detection rule;
- extracted fields;
- expected warnings;
- output records;
- safety limitations.

## Expert extension

Map the public-change path:

1. Model changes, if persistent fields are needed.
2. Service orchestration in `caereflex/services.py`.
3. CLI command or option, if public.
4. REST route or schema change, if public.
5. Exporter updates, if output changes.
6. Tests for adapter, CLI, REST, exporters, and security.
7. Wiki and reference documentation updates.

## Assessment checklist

- [ ] The learner can describe adapter boundaries.
- [ ] The learner avoids solver execution and unsafe engineering claims.
- [ ] The learner includes tests and docs in the design.
- [ ] The learner understands when service, CLI, REST, and exporter changes are required.
