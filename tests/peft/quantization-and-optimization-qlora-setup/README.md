# QLoRA Setup

## User Persona
The user is an LLM finetuning practitioner trying to fit a larger model on limited GPU memory.

## Scenario Coverage
- Skill area: `quantization-and-optimization`
- Capability: bitsandbytes 4-bit loading, `prepare_model_for_kbit_training`, QLoRA target modules, merge caveats
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/quantization-and-optimization/SKILL.md`, `skills/peft/sub-skills/quantization-and-optimization/references/quantized-training.md`, `skills/peft/sub-skills/quantization-and-optimization/scripts/check_quantized_peft.py`
- Trigger expectation: The prompt names QLoRA, bitsandbytes, PEFT, and quantized deployment caveats.

## Expected Successful Behavior
The agent should provide `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", ...)`, call `prepare_model_for_kbit_training` before `get_peft_model`, use `LoraConfig(target_modules="all-linear", task_type=TaskType.CAUSAL_LM, ...)`, and caution that quantized merge support depends on the quantizer.

## Failure Signals
The answer fails if it omits `prepare_model_for_kbit_training`, targets only arbitrary layers without explaining QLoRA all-linear targeting, ignores CUDA/library compatibility, or says all quantized adapters can be merged.
