---
name: slime-checkpoint-conversion
description: "Guides agents through slime checkpoint conversion between Hugging Face, Megatron torch_dist, FP8, and INT4 formats."
disable-model-invocation: true
---

# slime Checkpoint Conversion

Use this sub-skill when the user has Hugging Face weights but slime training needs Megatron `torch_dist`, or when a trained Megatron checkpoint must be exported back to Hugging Face.

## Short Workflow

1. Pick the model recipe from `slime-model-recipes`; conversion needs Megatron model-architecture args.
2. Verify the HF checkpoint has tokenizer/config files.
3. Convert HF to Megatron `torch_dist` before RL/SFT training.
4. After training, convert a saved Megatron iteration back to HF when the user wants normal inference/export.
5. For low-precision rollout/training, route to `slime-low-precision` after reading the basic conversion rules.

Read [references/workflows.md](references/workflows.md) for conversion recipes and checkpoint layout. Read [references/cli-reference.md](references/cli-reference.md) for bundled runner flags. Read [references/troubleshooting.md](references/troubleshooting.md) when conversion output cannot be loaded.

## Scripts

- Adapt [scripts/convert_hf_to_torch_dist.sh](scripts/convert_hf_to_torch_dist.sh), which calls the root bundled [../../scripts/convert_hf_to_torch_dist.py](../../scripts/convert_hf_to_torch_dist.py).
- Adapt [scripts/convert_torch_dist_to_hf.sh](scripts/convert_torch_dist_to_hf.sh), which calls the root bundled [../../scripts/convert_torch_dist_to_hf.py](../../scripts/convert_torch_dist_to_hf.py).
- Use root [../../scripts/inspect_model_recipe.py](../../scripts/inspect_model_recipe.py) to print bundled model args for common recipes.

## Required Inputs

- `HF_CHECKPOINT`: local Hugging Face model directory.
- `MEGATRON_SAVE`: output directory for `torch_dist`.
- `MEGATRON_PATH`: full Megatron-LM checkout on `PYTHONPATH`.
- Model args matching the exact architecture and tokenizer config.

## Handoff

After conversion, use the converted path as:

```bash
--ref-load /path/to/model_torch_dist
--load /path/to/save_or_resume_dir
--save /path/to/save_or_resume_dir
--hf-checkpoint /path/to/hf_checkpoint
```
