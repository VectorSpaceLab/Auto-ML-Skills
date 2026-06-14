# YAML SFT Config

## User Persona
A user who prefers command-line workflows and wants reproducible TRL jobs.

## Scenario Coverage
- Skill area: `cli-training`
- Capability: YAML config, `trl sft --config`, common SFT flags
- Difficulty: basic
- Prompt file: `user_request.txt`
- Expected references/scripts: `cli-training/SKILL.md`, `cli-training/references/cli-reference.md`
- Trigger expectation: The prompt says TRL, SFT command, YAML config, and launch command.

## Expected Successful Behavior
The agent should output a valid YAML config with the requested values and `packing: true`, then show `trl sft --config <file>.yaml`. It should mention checking `trl sft --help` for current flags and avoid unnecessary Python trainer code.

## Failure Signals
The response omits requested values, produces invalid YAML, uses Python-only config, or forgets the launch command.
