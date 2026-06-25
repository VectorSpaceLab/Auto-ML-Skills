# Maintenance Guide

## Purpose

Read this when adding, refreshing, renaming, replacing, merging, or removing an
imported repo skill from `repo-skills-router`. The goal is progressive
disclosure: keep the root router small, route first by practical usage scenario,
and put repo-level differences and selection guidance on the relevant scenario
pages.

## Update Workflow

Use the live SkillQED user copy at
`~/.skillqed/agent/skills/repo-skills-router/` as the primary writable router.
Do not update another same-named `repo-skills-router` directory before this live
copy has been updated. Do not push router changes into another agent tool from
this maintenance workflow. Export or merge into another agent only through the
dedicated `import-repo-skills-to-agent` meta skill after the user explicitly asks for
that target tool.

All maintenance that is part of an approved or auto-authorized SkillQED import
must run inside the global import lock provided by the
`verify-repo-skill` meta skill's `scripts/with_import_lock.mjs` helper.
The lock is rooted at `$SKILLQED_CODING_AGENT_DIR/locks/repo-skills-import.lockdir`
when `SKILLQED_CODING_AGENT_DIR` is set, otherwise
`~/.skillqed/agent/locks/repo-skills-import.lockdir`. It must cover the runtime
skill copy, first-time router creation from the template, fresh metadata and
skill-root reads, generated router writes, stale-file removal, and post-write
validation.

Do not hand-edit router Markdown as the import mechanism. The import transaction
must call `scripts/update_repo_skills_router.mjs` after copying the runtime skill
directory and writing or updating the skill's
`references/repo-routing-metadata.json`.

Inside the locked transaction:

1. Copy only the verified runtime skill directory into
   `~/.skillqed/agent/skills/<skill-id>/`.
2. Ensure that `<skill-id>/references/repo-routing-metadata.json` exists and
   contains the skill's structured usage-scenario routing metadata.
3. Run `node scripts/update_repo_skills_router.mjs --agent-dir <agent-dir> --already-locked`.
4. Let the updater re-read the live skills root, rebuild
   `repo-skills-router/SKILL.md`, `references/usage-scenarios.md`,
   `references/maintenance.md`, `references/scenario-registry.json`, and
   `references/scenarios/*.md`, remove legacy side-channel router files, and
   validate coverage and links before success.

## Scenario Registry

`references/scenario-registry.json` is the authoritative organization layer.
It defines canonical scenario IDs, aliases for overly narrow or historical
scenario IDs, and scenario-level selection guidance. During import, the updater
normalizes metadata scenario IDs through this registry before rendering
Markdown. If the registry has `enforce_known_scenarios: true`, new scenario IDs
are rejected unless the import metadata declares the scenario under top-level
`scenarios` with `allow_new: true`, `why_not_existing`, and
`expected_future_reuse`.

Prefer reusing a canonical scenario when a new repo overlaps an existing task
family. Create a new scenario only for a reusable task family that would be
misleading inside every existing scenario.

## Routing Metadata Shape

Each imported repo skill should include this generated metadata file:

```json
{
  "skills": {
    "example-skill": {
      "scenarios": [
        {
          "id": "example-workflows",
          "title": "Example Workflows",
          "when_to_read": "Requests about example repository workflows.",
          "role": "Explains how to use the example package for concrete tasks.",
          "read_when": "The request names the example package or asks for task patterns, APIs, CLIs, configs, artifacts, or errors owned by that package.",
          "best_for": "Setup, common workflows, and troubleshooting.",
          "avoid_when": "Another repo skill matches the user's task, package, data format, model family, or workflow more directly.",
          "useful_entry_points": ["example-skill/SKILL.md"],
          "selection_guidance": "Choose `example-skill` for example-package setup, workflow, API, config, artifact, or troubleshooting tasks, even when the user describes the task without naming the package."
        }
      ]
    }
  }
}
```

The managed updater also accepts an aggregate metadata file at
`<skills-root>/.repo-skills-router-metadata.json` for batch recovery workflows.
That aggregate file uses the same top-level `skills` object and may also include
a top-level `scenarios` object for shared scenario titles and selection
guidance.

## Entry Quality Bar

Each scenario entry should help a future agent decide quickly:

- what the repo skill does in this scenario;
- user terms, task intents, data/model formats, API/CLI surfaces, configs,
  artifacts, and errors that should route to it;
- when a different scenario or skill is better;
- which root/sub-skill/reference/script entry points to read next;
- how to choose among similar repo skills in the same scenario.

Do not make routing depend only on the user naming a package. Package names are
strong signals, but metadata should also describe the practical need or workflow
that implies the repo skill. Avoid ambiguous "Choose this skill" or "Choose it"
wording; name the concrete skill id or package in selection guidance.

## File Ownership

- `SKILL.md`: generated compact usage scenario quick map and routing
  instructions.
- `references/usage-scenarios.md`: generated scenario table, naming guidance,
  and page template.
- `references/scenario-registry.json`: generated or preserved canonical
  scenario registry used to normalize future imports.
- `references/scenarios/*.md`: generated scenario-specific repo skill entries,
  similar skill differences, and selection guidelines.
- `references/maintenance.md`: generated copy of this guide.

Do not put full repo skill documentation here. Name the repo skill and the entry
points to read; then read that repo skill's own `SKILL.md` for operational
details.
