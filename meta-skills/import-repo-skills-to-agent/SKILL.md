---
name: import-repo-skills-to-agent
description: "Use this skill when the user asks to import DisCo's managed skills, repo-specific skills, or repo-skills-router into another agent tool such as ~/.codex, ~/.agents, ~/.claude, or a project-local agent directory. Handles target skills-root detection, duplicate-skill overwrite questions, and repo-skills-router merging."
---

# Import Repo Skills To Agent

## Purpose

Use this meta skill to copy DisCo's managed skill library into another
agent tool. The source library is DisCo's managed user directory:
`~/.disco/agent/skills/` unless `DISCO_CODING_AGENT_DIR` points to a
different DisCo agent directory.

This skill is explicit export/import behavior. DisCo itself does not use
the managed repo skills in `~/.disco/agent/skills/` as runtime skills for
ordinary downstream tasks.

## Inputs

The user may provide only a tool root such as:

- `~/.codex`
- `~/.agents`
- `~/.claude`
- `/path/to/project/.agents`

Resolve the target skills root as follows:

1. Expand `~` and environment variables.
2. If the path basename is `skills`, treat it as the target skills root.
3. Otherwise, use `<tool-root>/skills` as the target skills root.
4. Create the target skills root only after confirming the source library is
   readable.

## Source Selection

The user may import the whole managed repo-skill library or a selected subset.
Selection terms may be directory ids, `name` frontmatter values, package/repo
names mentioned in `references/repo-provenance.md`, or a comma/space-separated
list with shell-style `*` wildcards. Resolve selection against the inventory
before copying and show the matched skill ids in the import plan.

If the user names specific packages or skills, import only those matched
non-router skills plus `repo-skills-router` when at least one repo skill is
included. If the user does not provide a package/skill filter, import every
valid skill directory under the DisCo managed skills root that has a direct
`SKILL.md`, including `repo-skills-router` when present.

Do not import review/test artifact directories, envs, prompts, extensions,
themes, sessions, or workflow run state. The source is only:

```text
<disco-agent-dir>/skills/<skill-id>/SKILL.md
<disco-agent-dir>/skills/<skill-id>/**/*
```

If `repo-skills-router` is missing from the DisCo managed skills root but
the bundled template is available, copy the bundled template into the import set
only when there are repo skills to route. Do not create an empty router as the
only imported skill unless the user explicitly asks for it.

## Pre-Import Validation

Before asking overwrite questions or copying files, refresh the DisCo managed
source library once by running
`verify-repo-skill/scripts/update_repo_skills_router.mjs --agent-dir
<disco-agent-dir>`. This is a repairable source-library maintenance step,
not a target import side effect: the updater must rebuild and validate
`repo-skills-router`, recover existing router entries when possible, and
backfill any missing per-skill `references/repo-routing-metadata.json` files
before strict validation. If the updater cannot prove complete routing coverage,
stop and report that source-library validation failed instead of silently
skipping repo skills.

Then inspect every selected skill directory:

1. Read `<skill-id>/SKILL.md` and parse its frontmatter.
2. Require frontmatter `name` to be present, lowercase-hyphen, no longer than
   64 characters, and equal to the directory basename.
3. Require a non-empty `description` line wrapped in double quotes.
4. For every non-router repo skill, require
   `disable-model-invocation: true` in the root `SKILL.md` and in every
   `sub-skills/<id>/SKILL.md`. If the source omits it, normalize the copied
   target only when the user explicitly authorizes normalization; otherwise
   skip that skill and report the validation failure.
5. For `repo-skills-router`, require that `disable-model-invocation: true` is
   absent so the router remains model-visible in the target agent.
6. For every selected non-router repo skill, require
   `references/repo-routing-metadata.json` unless the user explicitly imports a
   skill for manual use only and declines router participation.

Do not silently import invalid skills. Report validation failures by skill id,
source path, and exact reason. If the user selected a subset, a validation
failure in one selected skill should not block unrelated valid selections unless
the failed skill is required for the requested import.

## Duplicate Handling

Before copying, inspect the target skills root for existing skill directories.
Compare by directory basename and by the `name` frontmatter field in
`SKILL.md`.

For each non-router source skill that conflicts with a target skill:

1. Summarize the conflict using source path, target path, source frontmatter
   name, target frontmatter name, and a short evidence note if the contents look
   different.
2. Ask the user whether to overwrite the target copy. Use `ask_user_question`
   when available; otherwise ask in the conversation and wait.
3. If the user approves overwrite, replace only that target skill directory.
4. If the user declines overwrite, skip that skill and report it.

Never silently overwrite a non-router skill.

## Router Merge

Handle `repo-skills-router` specially. The source router used for target import
must be a filtered router for the selected import set, not a blind copy of the
full DisCo-managed router unless the user is importing the full managed
library.

For a subset import, build a temporary source-router view before touching the
target router:

```bash
node <disco-verify-skill>/scripts/update_repo_skills_router.mjs \
  --agent-dir <disco-agent-dir> \
  --include-skill <selected-skill-id> \
  --output-router-dir <temp-dir>/repo-skills-router
```

Repeat `--include-skill` or pass comma-separated ids for every non-router repo
skill that will actually be copied or overwritten in the target. Use this
temporary router as the source for the router copy or merge. Do not copy
`<disco-agent-dir>/skills/repo-skills-router/` directly for a subset import,
because that would expose unselected DisCo repo skills in the target router.

If the target has no router, copy the filtered source router into the target
skills root. If the target already has `repo-skills-router`, merge the filtered
source router with the target router instead of blindly replacing it.

Merge rules:

1. Read both routers' `SKILL.md`, `references/usage-scenarios.md`, and
   `references/scenarios/*.md` files.
2. Preserve target-only scenario rows and scenario pages.
3. Add source-only scenario rows and scenario pages from the filtered source
   router only. A source-only entry for an unselected DisCo repo skill is a bug;
   stop and rebuild the temporary source router with the exact selected ids.
4. For scenarios present in both routers, merge repo skill options by
   frontmatter name or directory id. Preserve target wording when it contains
   information not present in source, add source-only skill entries, and update
   `How To Choose` so similar skills from both routers have a concrete
   selection guideline.
5. If the same repo skill appears in both routers with conflicting guidance,
   ask the user whether the DisCo source entry should replace the target
   entry, the target entry should be preserved, or the entries should be merged.
6. Keep the two-layer structure: root quick map plus scenario pages. Do not
   introduce a separate similar-skill comparison file.
7. Preserve the normalized scenario entry fields: role, read_when, best_for,
   avoid_when, useful_entry_points, and selection_guidance. If a source skill's
   root description is too brief for routing, enrich the router entry from
   `references/repo-routing-metadata.json`, the nearest `SKILL.md`, and linked
   references rather than copying a one-line description into the scenario page.

After merging, verify that all scenario page links in `SKILL.md` and
`references/usage-scenarios.md` point to existing files.

## Copy Procedure

1. Resolve source and target paths.
2. Inventory source skill directories and target skill directories.
3. Apply any user-provided package/skill filters and validate the selected
   source skills before planning destructive operations.
4. Plan actions:
   - `copy`: target skill missing.
   - `overwrite`: target skill conflicts and user approved.
   - `skip`: user declined overwrite or source is invalid.
   - `merge-router`: both source and target have `repo-skills-router`.
5. Ask all required overwrite/merge conflict questions before making
   destructive changes.
6. Copy approved skills. Prefer directory-level replacement for approved
   overwrites, preserving permissions when possible.
7. Build a filtered source `repo-skills-router` for the exact non-router repo
   skills that were approved for copy/overwrite, then merge or copy that
   filtered router.
8. Re-validate the target copy:
   - non-router repo skills still contain `disable-model-invocation: true`;
   - `repo-skills-router` remains model-visible;
   - router links point to existing files;
   - selected skills are present and unselected skills were not modified;
   - the target router does not gain entries for unselected DisCo source
     skills, except for unrelated entries that already existed in the target
     router before this import.
9. Report imported, overwritten, skipped, and merged items with exact paths.

## Safety Checks

- Do not delete target skills that are not in the DisCo source library.
- Do not copy private envs, sessions, logs, auth files, package caches, or
  review/test artifacts.
- Do not write absolute local DisCo source paths into imported public skill
  content.
- If the target path is inside the DisCo source skills root, stop and tell
  the user that source and target are the same library.
- If a target conflict cannot be understood because `SKILL.md` is unreadable,
  ask before overwriting.
- Do not make all repo skills model-visible in the target agent. The
  `repo-skills-router` skill is the model-visible entry point; imported
  non-router repo skills should be hidden from automatic model invocation and
  read only after router selection or explicit user request.
- Do not let subset import leak all DisCo-managed repo skills through
  `repo-skills-router`. The router content imported from DisCo must be scoped
  to the selected skills that are actually present in the target.

## Handoff

End with a concise import summary:

- source DisCo skills root;
- target skills root;
- package/skill selection filters and matched skill ids;
- skills copied;
- skills overwritten after approval;
- skills skipped and validation or conflict reason;
- router action: copied, merged, unchanged, or unavailable;
- any manual follow-up needed, such as restarting the target agent so it reloads
  skills.
