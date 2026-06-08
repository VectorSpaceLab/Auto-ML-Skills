# Skills CLI Reference

Read this for TRL's built-in agent-skill management commands and Python API.

## Commands

```bash
trl skills list
trl skills list --target <agent-or-path> --scope project
trl skills install <skill> --target <agent-or-path> --scope project
trl skills install --all --target <agent-or-path> --scope global
trl skills install <skill> --target <agent-or-path> --force
trl skills uninstall <skill> --target <agent-or-path> --scope global
```

`trl skills list` without `--target` lists TRL skills bundled in the installed package. With `--target`, it lists installed skills in the resolved target directory.

## Target Resolution

Named agents:

| Agent | Project scope | Global scope |
| --- | --- | --- |
| `claude` | `./.claude/skills` | `~/.claude/skills` |
| `codex` | `./.codex/skills` | `~/.codex/skills` |
| `opencode` | `.opencode/skills` | `~/.config/opencode/skills` |

Custom paths are expanded and resolved directly:

```bash
trl skills install trl-training --target /path/to/skills
```

## Python API

```python
from trl.skills import list_agent_names, list_skills, resolve_target_path

print(list_agent_names())
print(list_skills())
print(resolve_target_path("codex", "global"))
```

Install/uninstall:

```python
from trl.skills import install_skill, uninstall_skill

install_skill("trl-training", target="codex", scope="project", force=False)
uninstall_skill("trl-training", target="codex", scope="project")
```

Exceptions include `FileNotFoundError` for missing skills, `FileExistsError` for existing target skills without force, `PermissionError` for write failures, and `ValueError` for invalid target/scope combinations.

## Bundled Skill

Current TRL source includes a bundled `trl-training` skill for CLI-based TRL training. It covers `trl sft`, `trl dpo`, `trl grpo`, `trl kto`, `trl rloo`, and `trl reward`.

This generated `trl` skill is broader: it covers Python APIs, data/rewards, vLLM/distributed, experimental code, and skills management in addition to CLI training.
