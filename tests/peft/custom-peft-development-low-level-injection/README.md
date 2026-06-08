# Low-Level Injection

## User Persona
The user is a library integrator who needs PEFT layers without changing the public model wrapper type.

## Scenario Coverage
- Skill area: `custom-peft-development`
- Capability: `inject_adapter_in_model`, `get_peft_model_state_dict`, `set_peft_model_state_dict`, tradeoffs
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/custom-peft-development/SKILL.md`, `skills/peft/sub-skills/custom-peft-development/references/custom-models-and-low-level-api.md`
- Trigger expectation: The prompt mentions low-level injection, LoRA, plain torch modules, adapter state dict, and avoiding `PeftModel`.

## Expected Successful Behavior
The agent should show `inject_adapter_in_model`, explain that it mutates the module in place, save with `get_peft_model_state_dict`, reload by injecting into a fresh model and calling `set_peft_model_state_dict`, and explain that full `PeftModel` conveniences such as adapter disabling/merging may not be available.

## Failure Signals
The answer fails if it uses only `get_peft_model`, claims low-level injection has all `PeftModel` utilities, or omits the two state-dict helper functions.
