# Install TRL Skill Into Codex

## User Persona
An agent tooling maintainer configuring skills for a project.

## Scenario Coverage
- Skill area: `agent-skills-management`
- Capability: `trl skills list/install/uninstall`, `codex` target, project/global scopes
- Difficulty: basic
- Prompt file: `user_request.txt`
- Expected references/scripts: `agent-skills-management/SKILL.md`, `references/skills-cli-reference.md`
- Trigger expectation: The prompt names TRL-provided agent skill, Codex, project/global scopes, and install/list/remove workflows.

## Expected Successful Behavior
The agent should show `trl skills list`, `trl skills install trl-training --target codex --scope project`, `trl skills uninstall trl-training --target codex --scope project`, explain project scope as `./.codex/skills` and global as `~/.codex/skills`, and mention `--force` only for overwriting.

## Failure Signals
The response confuses generated repo skill tests with TRL bundled skills, omits uninstall, ignores target scopes, or suggests destructive filesystem operations.
