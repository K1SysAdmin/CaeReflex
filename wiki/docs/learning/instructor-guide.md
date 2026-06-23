# Instructor Guide

Use this guide to teach CaeReflex in workshops, onboarding sessions, or academic modules.

## Teaching goals

A successful session should help learners:

- operate CaeReflex from the CLI;
- interpret structured evidence and warnings;
- explain the safe-use boundary;
- choose the right output for humans, agents, or APIs; and
- understand where developer extensions belong.

## 60-minute workshop

| Time | Activity |
| --- | --- |
| 0-10 min | Explain CaeReflex, ReflexCase, and the safety boundary |
| 10-30 min | Run [CLI-first Inspection](cli-first-inspection.md) |
| 30-45 min | Compare `caereflex.json`, `agent_context.json`, and Markdown report |
| 45-55 min | Write a safe summary and identify human follow-up checks |
| 55-60 min | Review common mistakes |

## Half-day workshop

1. Environment setup.
2. CLI-first inspection.
3. One domain project: Gmsh, OpenFOAM, or VTK.
4. CrossRef literature context with mock data.
5. Assessment discussion.

## Full-day technical workshop

1. CLI-first inspection.
2. OpenFOAM case review.
3. VTK result context.
4. CrossRef literature context.
5. REST/OpenAPI agent workflow.
6. Adapter extension design.
7. Group critique using the assessment rubric.

## Common learner mistakes

- Treating inspection as validation.
- Ignoring warnings because a command exited successfully.
- Giving agents full local paths instead of workspace-relative paths.
- Using live CrossRef calls when deterministic mock data is better for teaching.
- Forgetting to explain what a qualified engineer still needs to review.

## Facilitation prompts

Ask:

1. Which facts were extracted from files?
2. Which statements are assumptions?
3. Which warnings matter most to a reviewer?
4. Which output would you give to a human? Which to an agent?
5. What would be an unsafe claim?

## Instructor preparation checklist

- [ ] Confirm CaeReflex installs in the teaching environment.
- [ ] Run `caereflex examples list`.
- [ ] Run the CLI-first project once before class.
- [ ] Keep the safe-use policy visible during discussion.
- [ ] Use mock CrossRef responses for deterministic results.
- [ ] Decide whether REST/OpenAPI work is included or optional.
