---
name: repo-skills-router
description: "Use this two-layer router for imported repository skills. Read it when another agent needs to choose which repo-specific skill should inform a user request, when routing among similar repo skills, or after importing a repo skill to classify it by practical usage scenario and maintain selection guidance."
---

# Repo Skills Router

## Purpose

Use this skill as the maintained router for repo-specific skills imported into
DisCo's managed skill library. It helps another agent pick a relevant repo
skill as reference for a user request without reading every imported skill.

DisCo's bundled copy is only a template. The live writable router is the
user copy at `~/.disco/agent/skills/repo-skills-router/SKILL.md`, created
or updated after approved or auto-authorized imports. Do not edit the bundled
package copy as runtime state.

The router uses two-layer progressive disclosure:

1. `SKILL.md` gives a compact first-pass map from practical repository usage
   scenarios to scenario pages.
2. Each `references/scenarios/<scenario>.md` page explains which repo skills
   belong to that scenario, what each one is for, how similar repo skills differ,
   and how to choose among them.

## How To Route

1. Scan the usage scenario quick map below for the user's likely task family.
2. Read only the relevant scenario page listed in
   [references/usage-scenarios.md](references/usage-scenarios.md).
3. On that scenario page, compare the candidate repo skills by role,
   non-fit cases, overlap notes, and selection guideline.
4. Read the selected repo skill's own `SKILL.md` before relying on it.
5. If no scenario fits, fall back to the available skill descriptions, project
   context, or repository evidence. Do not invent a router entry.

Use this router only for selection. A router entry is not a substitute for the
selected repo skill's detailed instructions.

## Maintenance After Skill Import

When a verified repo-specific skill is imported after user approval, update the
live DisCo router by running the managed updater script described in
[references/maintenance.md](references/maintenance.md). Do not hand-edit router
Markdown as the import mechanism. The updater rebuilds this two-layer router
from live repo skills and structured `references/repo-routing-metadata.json`
files inside the global DisCo import lock.

Read [references/maintenance.md](references/maintenance.md), then:

1. Classify the imported skill into one or more practical usage scenarios in
   the skill's `references/repo-routing-metadata.json`. Reuse a canonical
   scenario or alias from
   [references/scenario-registry.json](references/scenario-registry.json)
   whenever one fits.
2. Include the repo skill's role, trigger terms, best-fit tasks, avoid-when
   notes, useful entry points, and selection guidance in that metadata.
3. Create a new scenario only when the registry would make the router
   misleading. In that case, declare the top-level `scenarios.<id>` entry with
   `allow_new: true`, `why_not_existing`, and `expected_future_reuse`.
4. In the locked import transaction, copy the runtime skill into
   `~/.disco/agent/skills/`, then run
   `verify-repo-skill/scripts/update_repo_skills_router.mjs
   --already-locked`.
5. Treat updater validation failure as import failure; fix the metadata or live
   skill directory before reporting import success.

## Usage Scenario Quick Map

Keep this section short. It should route a future agent to the right scenario
page, not document the repo skills in full.

<!-- DISCO_REPO_SKILLS_ROUTER_SCENARIOS:START -->
| Usage scenario | When to read | Scenario page | Representative repo skills |
| --- | --- | --- | --- |
<!-- DISCO_REPO_SKILLS_ROUTER_SCENARIOS:END -->
