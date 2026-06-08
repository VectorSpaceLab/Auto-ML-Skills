# PEFT Install Smoke Check

## User Persona
The user is new to PEFT and wants a reliable setup path before trying examples.

## Scenario Coverage
- Skill area: root skill
- Capability: package installation, public imports, core API verification
- Difficulty: basic
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/SKILL.md`, `skills/peft/scripts/check_peft_environment.py`, `skills/peft/references/api-reference.md`
- Trigger expectation: The prompt names Hugging Face PEFT, install commands, smoke checks, and LoRA APIs, which should trigger the root `peft` skill.

## Expected Successful Behavior
The agent should provide public install commands, a minimal Python import check using `peft`, `LoraConfig`, `TaskType`, and `get_peft_model`, and optionally suggest the bundled `check_peft_environment.py` diagnostic. It should not mention local inspection paths or conda prefixes.

## Failure Signals
The skill is too thin if the answer only says `pip install peft` without verification commands, omits dependency checks, gives local environment paths, or fails to point to the bundled diagnostic script.
