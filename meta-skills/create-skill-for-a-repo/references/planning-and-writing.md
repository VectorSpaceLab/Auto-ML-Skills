# Planning and Writing the Generated Skill

## Purpose

Read this reference after repository evidence discovery and installed-package inspection. It covers sub-skill boundaries, content inventory, coverage/depth planning, generated file writing, and common anti-patterns.

## Identify Sub-Skills

Split the repo into sub-skills only when the boundaries are useful for future agents. Good sub-skills usually map to:

- Distinct user workflows.
- Separate packages or major modules.
- Different CLIs, services, pipelines, or task families.
- Capabilities that require different references or scripts.

Keep sub-skills as functionally independent as possible. Do not group many orthogonal or relatively independent capabilities under one sub-skill just because they live near each other in the source tree.

Avoid creating sub-skills for tiny helper modules, internal-only implementation details, or arbitrary source folders.

## Build a Content Inventory

Before writing generated skill files, create a short content inventory from the research:

- User-facing workflows discovered in README, docs, examples, tests, notebooks, CLIs, and package metadata.
- Important public APIs, classes, functions, config objects, command-line entry points, and runtime facts verified from the installed package.
- Existing repo scripts or example programs that future agents could reuse only after they are copied, adapted, or wrapped into the generated skill.
- Public constraints, optional dependencies, required services, credentials, data files, Python versions, package extras, or hardware assumptions documented by the repo or verified from package metadata.
- Troubleshooting knowledge from issues in docs, test failure patterns, error messages, or user-provided notes.

## Coverage/Depth Matrix

Turn the inventory into a coverage/depth matrix before writing:

```text
Capability | Evidence source | Output location | Depth check
inference CLI | README, tests/test_cli.py | sub-skills/inference + references/cli-reference.md | enough commands, flags, inputs, outputs, and troubleshooting to use without reopening repo docs
model training | docs/training.md, examples/train.py | sub-skills/training + scripts/train_smoke_test.py | enough config, data format, API, and failure notes to run/adapt safely
```

Use this matrix to catch:

- Breadth failure: a public workflow, CLI, API family, documented example, test-backed behavior, or major module has no place in the generated skill tree.
- Depth failure: a capability is named, but the sub-skill lacks enough workflow steps, parameters, examples, bundled scripts, data/config assumptions, or troubleshooting for a future agent to use it without reopening source code or original docs.

## Target File Tree

Draft the target file tree before writing final bodies. For every planned file, include one sentence explaining its purpose:

```text
repo-name/
  SKILL.md - router, install, sub-skill map
  references/troubleshooting.md - cross-cutting install/import/runtime failures
  scripts/check_env.py - verifies importability and optional backend availability
  sub-skills/inference/SKILL.md - routes inference workflows
  sub-skills/inference/references/api-reference.md - verified inference signatures and parameters
  sub-skills/inference/scripts/smoke_test.py - minimal inference smoke test
```

Map each inventory item to exactly one output location. If an item is tightly coupled to one sub-skill, place it under that sub-skill's `references/` or `scripts/`, not the repo root. Use repo-level `references/` and `scripts/` only for material shared across multiple sub-skills.

When the inventory mentions an original repo path, the target file tree must also name the bundled skill file that replaces it. If a repo script is too large, unsafe, or environment-specific to bundle, extract the reusable parts into a smaller skill script or a reference recipe, and note any omitted side effects or prerequisites.

## Write Generated `SKILL.md` Files

For the generated repo skill:

- Keep the root `SKILL.md` concise and router-like.
- Include package installation instructions, required extras, editable install notes when useful, public prerequisites, and a minimal import check.
- Cover all user-facing repo capabilities across the root skill, sub-skills, references, and scripts.
- Give every sub-skill a focused `SKILL.md` with clear trigger scenarios.
- Put long API notes, usage examples, and domain references in `references/*.md`.
- Include `troubleshooting.md` in repo-level or sub-skill `references/` whenever enough reliable troubleshooting knowledge is available.
- Put reusable checks, introspection helpers, adapted repo examples, smoke tests, or workflow automation in `scripts/`.
- Use the repo's own terminology consistently.
- Prefer verified package facts over inferred behavior.

Every generated `SKILL.md` should include valid YAML frontmatter:

```markdown
---
name: repo-or-sub-skill-name
description: "Specific third-person description with trigger terms broad enough for natural user requests."
---
```

Quote string values with double quotes whenever they contain a colon, hash, bracket, brace, leading special character, or other YAML-sensitive content. Prefer quoting every `description` value by default. If the quoted string itself contains double quotes, escape them as `\"`.

Do not include `disable-model-invocation: true` in generated root or sub-skill frontmatter by default. The generated skill is meant to be discoverable and invoked automatically from natural user requests. Include `disable-model-invocation: true` only when the user explicitly asks for a generated skill that must require direct, manual invocation.

## Write References

For `references/`:

- Create reference files before or alongside the nearest `SKILL.md`, not as an afterthought.
- Use descriptive names such as `api-reference.md`, `workflows.md`, `cli-reference.md`, `configuration.md`, `data-formats.md`, `model-overview.md`, `benchmarks.md`, and `troubleshooting.md`.
- Structure reference files for future agent use: short purpose, when to read, verified facts, examples, and gotchas.
- Prefer distilled, task-oriented reference material over verbatim copies of long repo docs.

## Write Scripts

For `scripts/`:

- Prefer adapting or wrapping proven repo scripts and examples over inventing new helpers from scratch.
- Bundle every script that a generated `SKILL.md` tells future agents to run.
- Ensure linked script paths resolve inside the generated skill directory, not inside the original repo checkout.
- Include a shebang when appropriate and a top-level comment or docstring with purpose, prerequisites, and example invocation.
- Keep scripts deterministic and safe by default. Avoid network calls, downloads, training runs, destructive writes, or credential use unless the user explicitly wants that behavior.
- Link each script from the nearest `SKILL.md` and say whether future agents should run it, read it, or adapt it.

## Anti-Patterns

Avoid:

- A single-file repo skill for a repo with multiple user-facing workflows.
- A 400+ line sub-skill `SKILL.md` with thin or missing `references/`.
- A README summary that lacks verified API details, practical workflows, scripts, or troubleshooting.
- Reference links that point to files that were not created.
- Instructions that require future agents to run or read scripts, docs, examples, notebooks, or configs from the original repo checkout instead of bundled skill files.
- Mentions of the user's temporary Python environment.
- Generated `SKILL.md` frontmatter that disables model invocation when the user did not explicitly ask for manual-only invocation.
- Uppercase, underscored, dotted, spaced, or otherwise invalid skill identifiers in generated directory names, frontmatter `name` fields, or `evals/evals.json` `skill_name`.
- Invalid YAML frontmatter, especially unquoted string values containing colons.
- Copying entire docs pages into `SKILL.md` instead of restructuring them for agent use.
