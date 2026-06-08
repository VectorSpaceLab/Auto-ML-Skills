---
name: agent-skills-management
description: "Use TRL's built-in agent-skill management CLI and Python utilities to list, install, uninstall, and resolve skills for Claude, Codex, OpenCode, or custom skill directories."
---

# Agent Skills Management

Use this sub-skill when a user asks about `trl skills`, installing TRL-provided agent skills, listing target skill directories, or using `trl.skills` Python utilities.

## CLI

List TRL skills bundled with the package:

```bash
trl skills list
```

List skills installed in a target:

```bash
trl skills list --target codex --scope global
trl skills list --target ./.codex/skills
```

Install a skill:

```bash
trl skills install trl-training --target codex --scope project
```

Install all bundled skills:

```bash
trl skills install --all --target codex --scope global
```

Overwrite an existing installed skill:

```bash
trl skills install trl-training --target codex --scope global --force
```

Uninstall:

```bash
trl skills uninstall trl-training --target codex --scope global
```

Read [references/skills-cli-reference.md](references/skills-cli-reference.md) for target resolution and Python APIs.

## Target Names

TRL recognizes agent targets:

- `claude`
- `codex`
- `opencode`

Scopes are:

- `project`: project-local agent skill directory such as `./.codex/skills`.
- `global`: user-level agent skill directory such as `~/.codex/skills`.

A custom path can be used instead of a named target.

## Python Utilities

```python
from trl.skills import (
    install_skill,
    list_agent_names,
    list_skills,
    resolve_target_path,
    uninstall_skill,
)
```

Use Python utilities for tooling, tests, or custom installers. Use the CLI for normal user-facing instructions.

## Safety

- Installing with `--force` overwrites an existing skill directory.
- Project scope writes relative to the current working directory.
- Global scope writes into a user-level skills directory.
- After installation, the user may need to restart the target AI agent for discovery.
