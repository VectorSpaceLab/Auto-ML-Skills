---
name: create-skill-for-a-repo
description: "Creates a repo-specific Agent Skill from a local repository by inspecting source files and an installed Python package environment. Use when the user asks to create a skill for a repo, generate repo-specific skills, analyze a local Python package, or build skills for Claude Code, Codex, or similar coding agents."
disable-model-invocation: true
---

# Create Skill for a Repo

## Purpose

Use this skill to create a high-quality, repo-specific Agent Skill for Claude Code, Codex, Cursor, or similar coding agents.

The user must provide:

- A local repository path.
- A temporary Python environment where the package from that repository has already been installed for inspection.

The user may also provide a preferred generated-skill output path, a preferred usability-test-case output path, the installed package name, and known troubleshooting notes. If no output path is provided, default to creating the generated skill under the repository's own `skills/` directory.

The installed Python environment is required so the agent can inspect live APIs, function signatures, modules, imports, CLI entry points, and runtime behavior instead of relying only on source-code guesses. Treat this environment as private research context. It must not appear in the generated repo skill.

## Reference Map

Read these references as the workflow reaches each stage:

- [references/input-output-and-structure.md](references/input-output-and-structure.md): input collection, canonical skill ids, output path resolution, default `skills/` and `tests/` locations, generated skill tree, and content placement rules.
- [references/repository-evidence.md](references/repository-evidence.md): how to discover source roots, docs, examples, scripts, tests, configs, existing repo-local skills, and evidence maps before extracting skills.
- [references/installed-package-inspection.md](references/installed-package-inspection.md): read-only inspection of the user-provided installed package environment and how to avoid leaking local environment details.
- [references/planning-and-writing.md](references/planning-and-writing.md): sub-skill boundaries, coverage/depth matrix, target file tree planning, generated `SKILL.md` frontmatter, references, scripts, and anti-patterns.
- [references/usability-test-cases.md](references/usability-test-cases.md): usability test case directories that simulate realistic future users, including default `skills/tests/<skill-id>/` placement and required `user_request.txt` plus `README.md` files.
- [references/evaluation-verification-and-handoff.md](references/evaluation-verification-and-handoff.md): self-refine eval flow, verification checklist, creation report, publication notes, and quality bar.

## Required Workflow

1. Gather the repository path and Python inspection environment. Confirm the package is installed in that environment. If it is missing, stop and ask for an environment with the repo package installed.
2. Read [references/input-output-and-structure.md](references/input-output-and-structure.md). Resolve the canonical skill id, active skills root, generated skill directory, and usability test case directory before writing files.
3. Read [references/repository-evidence.md](references/repository-evidence.md). Build a short evidence map from package metadata, source roots, docs, examples, scripts, tests, configs, and existing repo-local skills. Do not require the user to enumerate these directories.
4. Read [references/installed-package-inspection.md](references/installed-package-inspection.md). Use the provided Python environment for read-only import, signature, docstring, module, CLI, and runtime fact inspection.
5. Read [references/planning-and-writing.md](references/planning-and-writing.md). Identify useful sub-skill boundaries, create a coverage/depth matrix, draft the target file tree, then write the generated repo skill, bundled references, and bundled scripts.
6. Read [references/usability-test-cases.md](references/usability-test-cases.md). After creating the generated skill, write usability test case directories under the user-specified test directory or, by default, `<active-skills-root>/tests/<chosen-skill-id>/`.
7. Read [references/evaluation-verification-and-handoff.md](references/evaluation-verification-and-handoff.md). Run a lightweight self-refine review, verify the generated skill and test cases, revise gaps, and report the handoff with a short creation report.

## Non-Negotiables

- Do not create generated skill content that depends on the original repository checkout remaining available. Copy, distill, adapt, or wrap source repo material into the generated skill's own `references/` or `scripts/`.
- Do not leak the user's local Python executable, activation command, virtualenv or conda name, machine-specific paths, local checkout path, or `pip show` installation location into generated public skill files.
- Do not overwrite or merge into an existing skill directory unless the user explicitly asks to update that exact skill.
- Do not treat `skills/tests/` as an existing skill directory. It is a usability-test-case area.
- Prefer verified package facts over guesses. Use docs, examples, and tests for intent; use source code and installed-package inspection to confirm API and runtime claims.
- Keep generated root and sub-skill `SKILL.md` files router-like. Move API tables, workflow depth, CLI catalogs, model lists, data schemas, long examples, and troubleshooting matrices into the nearest bundled `references/`.

## Output Summary

By the end, the user should have:

- A generated self-contained repo skill directory containing `SKILL.md`, and when useful, `sub-skills/`, `references/`, and `scripts/`.
- Usability test case directories in the configured test case directory, defaulting to `<active-skills-root>/tests/<chosen-skill-id>/`.
- Optional `evals/` development artifacts inside the generated skill only when practical for self-refine review.
- A final handoff that distinguishes public skill content, usability test cases, optional `evals/` artifacts, repo evidence used, generated sub-skills, and generated test-case coverage.
