# Merge Three Adapters

## User Persona
The user is experienced with PEFT and wants multi-adapter inference composition.

## Scenario Coverage
- Skill area: `adapter-loading-and-composition`
- Capability: named adapter loading, `add_weighted_adapter`, active adapter selection, `merge_and_unload` tradeoffs
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/adapter-loading-and-composition/SKILL.md`, `skills/peft/sub-skills/adapter-loading-and-composition/references/composition-and-merging.md`
- Trigger expectation: The prompt mentions multiple LoRA adapters, weighted merge, activation, and `merge_and_unload`.

## Expected Successful Behavior
The agent should show `PeftModel.from_pretrained(..., adapter_name=...)`, `load_adapter`, `add_weighted_adapter`, `set_adapter`, and discuss `merge_and_unload` only when the user wants a standalone full model and the method/quantization path supports merging.

## Failure Signals
The answer fails if it forgets adapter names, does not activate the merged adapter, claims merging always works, or confuses weighted adapter creation with saving a full merged base model.
