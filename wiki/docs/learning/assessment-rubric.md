# Assessment Rubric

Use this rubric for self-study, onboarding, classroom review, or pull-request review of learning materials.

| Area | Beginner | Competent | Advanced | Expert |
| --- | --- | --- | --- | --- |
| Workflow execution | Runs the documented commands | Explains each command's purpose | Adapts commands to a new local case | Designs a repeatable workflow for a team |
| Evidence interpretation | Finds outputs and basic fields | Separates extracted facts from warnings | Explains provenance and uncertainty | Critiques evidence limits and missing review steps |
| Safety boundary | Repeats that CaeReflex is not a validator | Avoids validation, certification, and safety claims | Corrects unsafe summaries | Designs agent/developer prompts that preserve constraints |
| CLI and exports | Creates JSON or Markdown outputs | Chooses the right export for a user | Compares full case JSON and agent context | Traces exporter responsibilities in the architecture |
| REST/OpenAPI | Recognizes health and schema endpoints | Imports a case and retrieves context | Designs a bounded tool-calling workflow | Reviews API exposure, authentication, and workspace risks |
| Developer architecture | Identifies adapters and services | Explains the service layer's role | Designs a safe adapter change | Plans tests, docs, and safety validation for a new feature |

## Minimum completion standard

A learner should be able to provide:

- the commands they ran;
- the files or endpoints they inspected;
- one extracted fact;
- one limitation or inspection flag;
- a safe summary that does not claim validation, convergence, mesh adequacy, certification, or design safety.

## Instructor review prompts

Ask learners:

1. What evidence came directly from files?
2. What did CaeReflex infer or summarize?
3. What would a qualified engineer still need to verify?
4. Which output would you give to an LLM agent, and why?
5. What statement would be unsafe or unsupported?
