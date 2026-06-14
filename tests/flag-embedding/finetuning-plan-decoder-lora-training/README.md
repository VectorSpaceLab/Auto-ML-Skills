# Finetuning Plan Decoder LoRA Training

## User Persona
ML engineer fine-tuning a large decoder-only embedding model.

## Scenario Coverage
- Skill area: finetuning
- Capability: decoder-only embedder module selection, LoRA flags, OOM mitigation
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/finetuning/SKILL.md`, `sub-skills/finetuning/references/training-workflows.md`, `sub-skills/finetuning/references/troubleshooting.md`
- Trigger expectation: The prompt names LoRA fine-tuning and a supported decoder-only embedding model.

## Expected Successful Behavior
The agent should choose `FlagEmbedding.finetune.embedder.decoder_only.base`, include `--use_lora`, LoRA rank/alpha/target modules, instruction format, `torchrun --nproc_per_node 2`, and OOM adjustments such as batch size, max lengths, gradient accumulation, LoRA, and checkpointing.

## Failure Signals
The agent uses an encoder-only module, omits LoRA flags, enables flash attention without caveats, or fails to validate data first.
