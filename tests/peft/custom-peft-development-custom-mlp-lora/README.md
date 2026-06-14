# Custom MLP LoRA

## User Persona
The user is a PyTorch developer applying PEFT to a custom model.

## Scenario Coverage
- Skill area: `custom-peft-development`
- Capability: custom `torch.nn.Module`, `named_modules`, `target_modules`, `modules_to_save`, save/load smoke test
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/custom-peft-development/SKILL.md`, `skills/peft/sub-skills/custom-peft-development/references/custom-models-and-low-level-api.md`, `skills/peft/sub-skills/custom-peft-development/scripts/smoke_custom_lora.py`
- Trigger expectation: The prompt names a plain PyTorch MLP, LoRA, target names, and save/load.

## Expected Successful Behavior
The agent should show `named_modules()` inspection, configure `LoraConfig(target_modules=[...], modules_to_save=[...])`, wrap with `get_peft_model`, verify trainable parameters, run a tiny forward/backward, save with `save_pretrained`, and reload with `PeftModel.from_pretrained` on a fresh base instance.

## Failure Signals
The answer fails if it assumes Transformers auto target mappings, omits `modules_to_save` for the output layer, or does not show a save/load verification path.
