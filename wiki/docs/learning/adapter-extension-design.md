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

## Step-by-step adapter design algorithm

Use this algorithm before adding or changing code in `caereflex/adapters/`. The goal is to make a new adapter predictable for `caereflex/services.py`, safe for untrusted workspaces, honest about evidence quality, and visible through exporters and public interfaces.

### 1. Artefact detection

1. Name the artefact family in user language and code language. For example, decide whether the adapter represents one file type, a folder convention, a solver case, a post-processing result, or a mixed bundle.
2. List every detection signal in priority order:
   - exact file names, such as solver dictionaries or manifest files;
   - suffixes, such as `.vtk`, `.vtu`, `.msh`, `.geo`, `.step`, or equivalent new formats;
   - folder landmarks, such as `system/controlDict`, `constant`, or `0` for OpenFOAM-style cases;
   - file-header magic bytes or short textual signatures;
   - optional metadata files that improve confidence but are not required.
3. Decide whether auto-detection belongs in `caereflex/services.py` `detect_adapter()` or only in an explicit adapter selection path. Add auto-detection only when false positives are unlikely and the signal is cheap to check.
4. Define a deterministic conflict rule. If two adapters can match the same directory, prefer the most specific landmark over broad suffix scanning, and record the ambiguous evidence as an inspection flag rather than silently switching behavior.
5. Map the detection result to `ReflexCase.case_type`, `detected_formats`, `detected_tools`, and `physics_tags` from `caereflex/core/models.py`. Add model enum values only when the public schema genuinely needs a stable new type.

### 2. Bounded file discovery

1. Choose a workspace root before scanning. A single-file adapter usually uses the file parent; a case-folder adapter usually uses the selected folder.
2. Convert every user-visible path through safe display rules instead of exposing absolute local paths. Existing adapters use `safe_display_path()` before placing paths into `SourceFileRecord.relative_path`, traces, warnings, and provenance details.
3. Bound discovery by count, depth, suffix, and size:
   - respect `CaeReflexConfig.max_scan_files`;
   - respect `CaeReflexConfig.max_scan_depth` for recursive designs;
   - filter by expected suffixes or exact relative paths before expensive inspection;
   - avoid reading or hashing files larger than `CaeReflexConfig.max_file_size_bytes` unless the design explicitly justifies a streaming binary reader.
4. Fill `ReflexCase.workspace` with `root_display`, `scan_depth`, `file_count_considered`, and the active limits so a user can explain why evidence may be incomplete.
5. Treat skipped files as part of the inspection result. A scan-limit hit, depth-limit hit, skipped-large hash, or unsupported suffix should produce either an `InspectionFlag` or a clear provenance detail.

### 3. Safe text or binary inspection

1. Start from read-only operations. An adapter must not execute solvers, load user scripts as Python modules, shell out to project files, or mutate the case directory.
2. Pick the narrowest parser that can extract the intended facts:
   - for text, read with explicit encoding and safe error handling, then parse named patterns or structured blocks;
   - for binary, read magic bytes, headers, and bounded chunks before considering a dependency parser;
   - for optional dependency parsers, degrade to fingerprint-only inspection when the dependency is missing.
3. Hash source files with `sha256_file()` when within the configured size limit, and store the resulting `HashStatus` in `SourceFileRecord`.
4. Never convert parser success into engineering validation. A valid syntax parse can support facts such as field names, declared patch names, or declared mesh counts, but it cannot prove convergence, mesh adequacy, certification, safety, or physical correctness.
5. Keep inspection deterministic. Do not make network calls from adapters; use separate services such as CrossRef enrichment for external metadata.

### 4. Extracted versus inferred facts

1. Classify each output field before implementation:
   - **extracted** means the fact is directly present in a source artefact, such as a declared boundary patch, field name, cell count from a mesh file, or solver setting;
   - **inferred** means CaeReflex derived a tentative interpretation from file names, folder layout, heuristics, or partial evidence;
   - **generated** means CaeReflex created bookkeeping data, such as IDs or timestamps;
   - **external metadata** means the value came from a service outside the inspected artefact set.
2. Encode that classification in `TraceInfo.source_kind` from `caereflex/core/models.py` for every `EngineeringAsset`, `BoundaryConditionRecord`, `MaterialPropertyRecord`, `NumericalSettingsRecord`, `ResultFieldRecord`, and other record you populate.
3. Keep inferred facts out of extracted-fact sections when possible. `caereflex/exporters.py` separates `extracted_facts` and `inferred_facts` in the agent-context export by inspecting trace source kind.
4. Attach `source_files`, `adapter`, `confidence`, and concise notes to traces. If confidence is below 1.0, explain why the fact is heuristic or incomplete.
5. Prefer omission plus a warning over overconfident inference. If a fact cannot be supported by inspected evidence, do not create the record.

### 5. Warning and inspection-flag generation

1. Define warning categories before coding. Reuse patterns such as `path_not_found`, `unsupported_format`, `dependency_missing`, `best_effort_geometry`, `scan_limit_reached`, `file_too_large`, `parse_partial`, and `ambiguous_detection` where they fit.
2. Use `InspectionFlag` with `Severity.info`, `Severity.warning`, or `Severity.error` from `caereflex/core/models.py`:
   - `info` for expected best-effort limitations;
   - `warning` for partial evidence, skipped optional inspection, dependency gaps, or heuristics;
   - `error` for missing paths, unreadable required files, unsupported artefacts, or failed mandatory parsing.
3. Set adapter and inspection status consistently:
   - `success` when required evidence was inspected without material flags;
   - `partial_success` when useful evidence exists but limits, warnings, or optional failures occurred;
   - `failed` or `unsupported` when no reliable case can be created.
4. Put human-facing warning text in both `AdapterResult.warnings` when useful to callers and `ReflexCase.inspection_flags` when the warning should travel with exports.
5. Add `agent_summary.do_not_claim` entries for limitations that downstream agents and reports must preserve.

### 6. Provenance recording

1. Add a start event before inspection and a completion event after status is known. Existing designs use `ProvenanceRecord(event="*_inspection_started", details={...})`; mirror that pattern with an adapter-specific event name.
2. Record only safe, relative, or display paths in provenance details. Do not leak absolute workstation paths or secrets from environment-specific files.
3. Include detection evidence, active limits, parser mode, dependency fallbacks, and skipped-file counts in provenance details when those choices affect interpretation.
4. Ensure every model record has a trace that points back to the source file or states that it was generated. Provenance explains the inspection workflow; traces explain each fact.
5. Keep events stable enough for exporters and tests. If an event name becomes public through reports or agent context, treat it as a compatibility surface.

### 7. Model/schema impact

1. First try to express the new adapter with existing `caereflex/core/models.py` records: `SourceFileRecord`, `EngineeringAsset`, `SolverRecord`, `BoundaryConditionRecord`, `MaterialPropertyRecord`, `NumericalSettingsRecord`, and `ResultFieldRecord`.
2. Add enum values, record fields, or schema versions only when existing generic `metrics`, `properties`, or `metadata` fields would make the evidence ambiguous or hard to consume.
3. If adding schema fields, update validation, fixtures, serialization tests, and backward-compatibility expectations. Consider whether `schema_version` should change.
4. Keep optional fields optional when older adapters cannot populate them. Avoid forcing Gmsh, OpenFOAM, VTK, or future adapters to fabricate values.
5. Document field semantics, unit expectations, and source-kind rules in the developer guide and this lesson when a public schema changes.

### 8. CLI, REST, exporter, and docs impact

1. Services: register the adapter in `caereflex/services.py` `inspect_with_adapter()` and, if safe, in `detect_adapter()`. Confirm the adapter string, class name, and any alias are consistent.
2. CLI: add or update command choices, help text, examples, and error handling when users can select the adapter explicitly or trigger it through auto-detection.
3. REST: update request schemas, route documentation, response examples, and size-limit behavior if the web API exposes adapter names or accepted artefact types.
4. Exporters: update `caereflex/exporters.py` only when new records must appear in JSON, agent context, Markdown, BibTeX, or future export formats. Preserve safe-use policy and do-not-claim notes.
5. Docs: update architecture pages, the adapter developer guide, examples, and learning material. Include exact supported artefacts, inspection limits, warning categories, and sample output.
6. Public examples: add a minimal fixture that is small, license-compatible, deterministic, and safe to inspect without external programs.

### 9. Minimum test matrix

| Area | Minimum cases | Expected assertions |
| --- | --- | --- |
| Detection | explicit adapter, auto-detected file, auto-detected folder, ambiguous folder | Correct adapter name or clear unsupported/ambiguous flag from `caereflex/services.py`. |
| Bounded discovery | within limit, file-count limit, depth limit, large file | `WorkspaceInfo` limits are recorded; skipped files produce flags; no unbounded recursion occurs. |
| Text/binary safety | valid minimal artefact, malformed artefact, unreadable or oversized artefact | No execution or mutation; status is success, partial success, or failed as designed. |
| Extracted/inferred facts | direct declarations, heuristic names, missing facts | `TraceInfo.source_kind` is correct and unsupported facts are omitted. |
| Provenance | happy path and fallback path | Start/completion events, parser mode, and safe paths are present. |
| Model/schema | serialization and deserialization | `ReflexCase` round-trips through JSON with stable fields and enum values. |
| CLI | explicit and auto adapter commands | Exit codes, help text, output paths, and user warnings are correct. |
| REST | upload/inspect success and rejected request | Request limits, response schema, and errors match documented behavior. |
| Exporters | JSON, agent-context JSON/MD, Markdown report | Extracted and inferred sections, inspection flags, source files, and do-not-claim notes are preserved. |
| Docs/examples | published minimal fixture and tutorial command | Documentation commands run and generated examples match expected snapshots or structural assertions. |

A practical first pull request can implement adapter-unit tests, service detection tests, and JSON/exporter round-trip tests. Add CLI, REST, and documentation checks in the same change when the adapter is public through those surfaces.

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
