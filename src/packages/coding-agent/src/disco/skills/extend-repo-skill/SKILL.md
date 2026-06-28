---
name: extend-repo-skill
description: "Extends an existing repository-specific Agent Skill with new capabilities, deeper coverage, troubleshooting, scripts, and usability tests. Use when the user asks to expand, improve, deepen, or add coverage to an already implemented skill instead of creating a new skill from scratch. If the repository itself changed and the old skill may be stale, use refresh-repo-skill instead."
---

# Extend Repo Skill

## Purpose

Use this skill when the user already has a generated or hand-written Agent Skill and wants to expand it without losing the useful behavior it already provides.

Typical requests include:

- Add support for a new repo feature, public API, CLI, workflow, model family, config format, or troubleshooting path that the user specifically wants covered.
- Improve thin references, missing scripts, poor routing, incomplete usability tests, or unclear triggering.
- Extend an existing skill for a larger repo instead of regenerating it from scratch.

If the user's main concern is that the repository code, docs, APIs, CLIs,
configs, or dependencies changed and the old skill may be stale, use the sibling
`refresh-repo-skill` skill instead.

The expected result is an edited runtime skill directory plus updated
usability test cases and a verification/human-review package under the
skill's review/test artifact directory. Do not create a separate replacement
skill unless the user explicitly asks for a fork.

## Inputs

Gather or infer:

- Existing skill directory containing `SKILL.md`.
- Repository path used as the evidence source for the extension.
- The user's requested new capability, failure mode, coverage gap, or quality improvement.
- Python inspection environment and installed package name when live API verification is needed.
- Existing review/test artifact directory, if any.
- Desired review/test artifact output directory, if the user has a preference.

If the existing skill directory is missing or does not contain `SKILL.md`, stop and ask for the correct skill path.

## Reference Map

Read these references as the workflow reaches each stage:

- [references/extension-planning.md](references/extension-planning.md): scope capture, current-skill audit, repository evidence gathering, coverage-gap planning, and extension plan format.
- [references/editing-and-versioning.md](references/editing-and-versioning.md): editing rules, preserving existing behavior, frontmatter constraints, references/scripts updates, and usability-case expansion.
- [references/verification-and-handoff.md](references/verification-and-handoff.md): automatic verification, human review package, regression-sensitive checks, and final handoff.

When useful, also read sibling meta-skill references: `../create-repo-skill/references/` for canonical skill IDs, repository evidence discovery, installed-package inspection, planning, and writing, and `../verify-repo-skill/references/` for usability test-case format, verification review, and import/index routing guidance.

## Required Workflow

1. Resolve the existing skill directory, repository path, requested extension, and review/test artifact directory. If the user does not specify one, default to `<repository-path>/skills/tests/<skill-id>/`, with usability cases under `test-cases/` and review reports under `reports/`.
2. Read [references/extension-planning.md](references/extension-planning.md). Audit current root/sub-skill routing, bundled references, bundled scripts, evals, usability tests, and known gaps before editing.
3. Gather targeted repository evidence for the requested extension. Use source code plus installed-package inspection for API facts; use docs, examples, tests, and configs for intent and workflows.
4. Write a concise extension plan that maps each new or changed capability to exactly one skill location, reference, script, or usability case.
5. Read [references/editing-and-versioning.md](references/editing-and-versioning.md). Edit the existing skill in place while preserving useful current guidance, frontmatter IDs, and public structure.
6. Add or update usability test cases for the new capability and at least one regression-sensitive existing workflow under `test-cases/` in the review/test artifact directory.
7. Read [references/verification-and-handoff.md](references/verification-and-handoff.md). Run automatic verification, create a human review package under `reports/` in the review/test artifact directory, fix blocking issues, and report the handoff.

## Non-Negotiables

- Do not discard and rewrite the whole skill just because the extension is easier to express from scratch.
- Do not rename root or sub-skill IDs unless the user explicitly asks or the current names are invalid.
- Do not remove existing references, scripts, routes, or usability cases unless they are wrong, stale, duplicated, or replaced by a better self-contained artifact.
- Do not add claims about APIs, CLIs, configs, data formats, or runtime behavior without repository evidence or live inspection.
- Do not leak local checkout paths, Python executable paths, virtualenv or conda names, `pip show` locations, or machine-specific details into public skill files.
- Do not link runtime skill documentation to original repo docs, examples, notebooks, or scripts. Distill or adapt material into the skill directory.
- Do not leave new or existing runtime guidance that tells future agents to run,
  read, or adapt source repo scripts by path. Bundle the needed script,
  wrapper, or distilled recipe inside the skill's own `scripts/` or
  `references/` tree before linking it.
- Do not treat `tests/` as a skill directory. It is the review/test artifact area.
- Do not write `evals/`, verification reports, human-review notes, publication checklists, prompt samples, benchmark notes, or other check-only artifacts inside the runtime skill directory. Put concrete usability cases under the review/test artifact directory's `test-cases/` subtree and reports under its `reports/` subtree, defaulting to `<repository-path>/skills/tests/<skill-id>/`.

## Output Summary

By the end, the user should have:

- The existing skill directory updated in place.
- New or revised references/scripts/sub-skills where the requested capability needs depth.
- Updated usability test cases in the configured review/test artifact directory's `test-cases/` subtree.
- An automatic verification report and human review package in the configured review/test artifact directory's `reports/` subtree.
- A final handoff that distinguishes changed public skill content, review/test artifacts, evidence used, and remaining gaps.
