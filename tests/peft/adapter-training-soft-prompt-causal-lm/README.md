# Soft Prompt Causal LM

## User Persona
The user is an NLP practitioner who knows causal LM training but not PEFT prompt methods.

## Scenario Coverage
- Skill area: `adapter-training`
- Capability: prompt tuning method selection, virtual token setup, `PromptTuningConfig`, training loop shape
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/adapter-training/SKILL.md`, `skills/peft/sub-skills/adapter-training/references/method-selection.md`, `skills/peft/sub-skills/adapter-training/references/workflows.md`
- Trigger expectation: The prompt asks for learned soft prompts and PEFT config choice.

## Expected Successful Behavior
The agent should choose `PromptTuningConfig` with `PromptTuningInit.TEXT`, set `task_type="CAUSAL_LM"`, compute `num_virtual_tokens` from the initialization phrase if appropriate, include `prompt_tuning_init_text` and `tokenizer_name_or_path`, wrap with `get_peft_model`, and sketch a Trainer or custom PyTorch loop.

## Failure Signals
The skill is insufficient if the answer defaults to LoRA, omits virtual token/tokenizer fields, treats prompt tuning like arbitrary module targeting, or lacks any training/verification steps.
