# SFT LoRA Recipe

## User Persona
A practitioner who knows Hugging Face training basics but does not know the TRL Python trainer API.

## Scenario Coverage
- Skill area: `core-trainers`
- Capability: SFTTrainer, SFTConfig, PEFT, conversational data, assistant-only loss
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/trl/sub-skills/core-trainers/SKILL.md`, `references/trainer-api.md`, `references/trainer-workflows.md`, root environment check script
- Trigger expectation: The prompt mentions TRL, Python, `SFTTrainer`, LoRA, chat messages, and assistant-only loss.

## Expected Successful Behavior
The agent should provide an SFT Python recipe using `SFTTrainer`, `SFTConfig`, and `peft.LoraConfig`; explain when to set `assistant_only_loss=True`; mention the chat-template generation-mask requirement; include a safe import or `minimal_trainer_imports.py` check; and avoid claiming that training runs without model/dataset downloads.

## Failure Signals
The response uses only CLI commands, ignores `messages` data, omits PEFT installation/config, recommends assistant-only loss without chat-template caveats, or references local/private environment paths.
