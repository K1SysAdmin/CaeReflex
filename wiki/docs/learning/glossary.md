# Glossary

## Adapter

A read-only inspector for a supported artefact family such as Gmsh, OpenFOAM, or VTK.

## Agent context

A compact export intended for LLM agents. It emphasizes safe-use policy, extracted and inferred facts, inspection warnings, provenance, and do-not-claim guidance.

## CrossRef metadata

Bibliographic metadata and available abstracts returned by CrossRef when explicitly requested. It is related-literature context, not proof that a simulation is correct and not evidence that full papers were read.

## Extracted fact

A fact derived from inspected files or explicit metadata. Extracted facts should still be interpreted in context and may be partial.

## Inferred fact

A tentative conclusion produced from inspected evidence. Inferred facts require more caution than extracted facts.

## Inspection flag

A warning, limitation, or review prompt produced during inspection. Flags may indicate missing evidence, skipped files, unsupported content, partial extraction, or safety-relevant limitations.

## Provenance

A record of what CaeReflex inspected, generated, exported, or attached. Provenance helps users trace evidence back to actions and sources.

## ReflexCase

The structured CaeReflex case record that stores inspected evidence, metadata, flags, provenance, exports, and agent-facing summaries.

## Safe-use policy

The rules that prevent users and agents from overstating what CaeReflex can prove. CaeReflex does not validate simulations, prove convergence, assess mesh adequacy, certify engineering results, or establish design safety.

## Workspace-relative path

A path interpreted relative to the configured CaeReflex workspace. Agents and REST workflows should prefer workspace-relative paths instead of arbitrary absolute host paths.
