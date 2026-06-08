# Input, Output, and Structure

## Purpose

Read this reference before writing any generated skill files. It defines the required inputs, optional inputs, path resolution rules, generated skill layout, and content placement rules.

## Required and Optional Inputs

Before creating files, confirm:

- Repository path.
- Python executable or environment activation command for temporary inspection only.
- Installed package name if it differs from the repo name.
- Target skill output path, if the user has a preference.
- Test case output path, if the user has a preference.
- Whether the skill should be personal, project-local, or exported as a standalone skill directory.
- Known troubleshooting notes, common failures, confusing errors, or operational pitfalls that should be captured.

If the Python environment is missing or the package is not installed, stop and ask the user to provide an environment with the repo package installed.

Do not require the user to enumerate source, docs, examples, scripts, or test directories. Discover those extraction inputs from the repository tree.

## Canonical Skill Id

Choose a canonical skill id before resolving the final file tree. It must match `^[a-z0-9][a-z0-9-]{0,63}$`:

- Lowercase letters, numbers, and hyphens only.
- Maximum 64 characters.
- No uppercase letters, underscores, spaces, dots, slashes, or leading hyphen.

Normalize by lowercasing, converting CamelCase boundaries and other separators to hyphens, collapsing repeated hyphens, and trimming hyphens. Use the canonical id as the default generated root directory basename and root `SKILL.md` frontmatter `name`.

Keep public project capitalization only in prose. For example, use `flag-embedding` as the generated skill id for a project publicly called `FlagEmbedding`, but use `FlagEmbedding` in prose when referring to the project branding.

## Generated Skill Output Path

Resolve the generated skill output path before writing files:

- If the user does not specify a target skill output path, set the active skills root to `<repository-path>/skills/`, create it if needed, and create the generated skill under that directory.
- If the user gives a directory that is clearly a skills root, such as a path ending in `skills/` or a request to create the skill "under" a directory, treat that directory as the active skills root and create a new generated skill subdirectory inside it.
- If the user gives a path that is clearly the exact generated skill directory, such as an existing skill directory containing `SKILL.md` or an explicit request to update/create that exact directory, treat its parent as the active skills root.
- If the requested path does not exist and its basename already looks like the intended skill id, treat it as the generated skill directory. Otherwise treat it as the active skills root. Ask a concise clarification only when both interpretations are plausible and would write to meaningfully different places.
- If `<repository-path>/skills/` or the active skills root already exists, inspect existing skill directories as additional evidence for local conventions, useful references, prior troubleshooting notes, and expected structure, but create the new repo skill in a new normalized subdirectory and never overwrite or merge into an existing skill directory unless the user explicitly asks to update that exact skill.

If the active skills root already contains a directory with the canonical skill id, choose a new non-conflicting normalized directory name such as `<canonical-id>-repo-skill` or `<canonical-id>-2`, then use that chosen directory basename consistently as the generated root `SKILL.md` frontmatter `name` unless the user asked to update the existing skill.

## Usability Test Case Output Path

If the user does not specify a test case output path, save generated skill usability test case directories under `<active-skills-root>/tests/<chosen-skill-id>/`. Create missing directories as needed.

If the user specifies a test case output path, use that directory exactly. Treat `tests/` as a test-case area, not as a generated skill directory.

The test case output path contains one directory per scenario, not standalone case markdown files. See `references/usability-test-cases.md` for the required `user_request.txt` and `README.md` case format.

## Generated Skill Shape

Create the generated skill as a self-contained directory for the target repository. For repos with multiple meaningful user-facing capabilities, use this shape:

```text
repo-name/
  SKILL.md                    # Router for the whole repo skill, not a full manual.
  sub-skills/                 # One directory per coherent sub-skill.
    sub-skill-1/
      SKILL.md                # Focused workflow router for this sub-skill.
      references/             # Markdown reference files for this sub-skill.
      scripts/                # Reusable scripts, with comments explaining usage.
  references/                 # Repo-level Markdown reference files.
  scripts/                    # Repo-level reusable shell, Python, or helper scripts.
```

For a very small repo with only one coherent user-facing workflow, it is acceptable to omit `sub-skills/` and keep one concise root `SKILL.md` plus bundled `references/` and `scripts/` when useful. Do not create artificial sub-skills just to match the tree shape.

Self-contained means future agents can use the generated skill after the original repository checkout is gone. Do not write generated instructions such as "run `examples/foo.py` from the repo" or "see `docs/bar.md` in the original repository." If source repo material is important, copy, distill, adapt, or wrap it into the generated skill's own `references/` or `scripts/`.

## Progressive Disclosure

- Root `SKILL.md`: target 80-150 lines. It should remain a router.
- Sub-skill `SKILL.md`: target 80-200 lines. If it approaches 250 lines, move detail into `references/`.
- API tables, model lists, benchmarks, long examples, CLI catalogs, troubleshooting matrices, and multi-page workflows over roughly 30 lines belong in `references/*.md`.
- Every reference or script must be linked from the nearest `SKILL.md` with one sentence explaining when to read or run it.
- Do not duplicate the same material in `SKILL.md` and references.

## Content Placement

| Content | Location |
| --- | --- |
| Repo purpose, install command, minimal import check, sub-skill routing | Root `SKILL.md` |
| Sub-skill purpose, triggers, short workflow, common decision points | Sub-skill `SKILL.md` |
| Full API signatures, parameter notes, object relationships | Nearest `references/api-reference.md` |
| End-to-end recipes, tutorials, notebooks, training or inference flows | Nearest `references/workflows.md` or a specific workflow reference |
| CLI commands, flags, config files, environment variables | Nearest `references/cli-reference.md` or `configuration.md` |
| Data formats, schemas, expected columns, dataset layouts | Nearest `references/data-formats.md` |
| Model catalogs, benchmark tables, supported backends, compatibility matrices | Nearest `references/model-overview.md`, `benchmarks.md`, or `compatibility.md` |
| Errors, confusing behavior, debugging steps, operational pitfalls | Nearest `references/troubleshooting.md` |
| Reusable environment checks, API inspection, smoke tests, repo example wrappers | Nearest `scripts/` directory |
| Cross-cutting checks used by several sub-skills | Root `scripts/` |

All locations in the table refer to files inside the generated skill directory. Original repo paths are research inputs, not runtime dependencies for the generated skill.
