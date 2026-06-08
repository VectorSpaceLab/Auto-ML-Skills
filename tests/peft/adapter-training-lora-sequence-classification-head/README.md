# LoRA Sequence Classification Head

## User Persona
The user is an applied ML engineer who knows Transformers but is unsure how PEFT handles task heads.

## Scenario Coverage
- Skill area: `adapter-training`
- Capability: `LoraConfig`, `TaskType.SEQ_CLS`, `modules_to_save`, trainable parameter verification, save/load awareness
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/adapter-training/SKILL.md`, `skills/peft/sub-skills/adapter-training/references/workflows.md`, `skills/peft/references/troubleshooting.md`
- Trigger expectation: The prompt mentions LoRA, Transformers sequence classification, adapter checkpoint reload, and trained head handling.

## Expected Successful Behavior
The agent should recommend `TaskType.SEQ_CLS`, include the classifier or equivalent task head in `modules_to_save`, call `get_peft_model`, verify trainable parameters, save with `save_pretrained`, and load with `PeftModel.from_pretrained` on a compatible base model. It should explain that `get_peft_model` is not the trained-adapter loading path.

## Failure Signals
The answer fails if it omits `modules_to_save`, uses `get_peft_model` to load trained weights, ignores the randomly initialized head, or gives architecture-specific target modules without telling the user to inspect the actual model.
