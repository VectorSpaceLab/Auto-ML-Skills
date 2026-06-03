---
name: slime-model-recipes
description: "Helps agents choose bundled slime Megatron model argument recipes and adapt Qwen, GLM, DeepSeek, Llama, GPT-OSS, Mimo, Moonlight, MiniMax, and Kimi variants."
disable-model-invocation: true
---

# slime Model Recipes

Use this sub-skill when a user needs model architecture arguments for conversion or training. slime's Megatron backend does not infer all architecture details from HF checkpoints, so recipe selection is part of every serious job.

## Short Workflow

1. Identify the exact model family and size from the HF checkpoint.
2. Check whether a bundled recipe covers it. Run root [../../scripts/inspect_model_recipe.py](../../scripts/inspect_model_recipe.py) with `--list`.
3. If covered, use the recipe output as `MODEL_ARGS`.
4. If the exact variant is not listed, adapt the closest bundled family recipe from HF `config.json` and known slime plugin requirements; read [references/model-overview.md](references/model-overview.md).
5. Override subtle differences explicitly, especially `--rotary-base`, vocab size, GQA groups, model plugin `--spec`, MoE parallelism, and attention backend.

Read [references/model-overview.md](references/model-overview.md) for model family mapping. Read [references/configuration.md](references/configuration.md) for how recipes are used in conversion/training. Read [references/troubleshooting.md](references/troubleshooting.md) when a recipe loads but generations are wrong.

## Scripts

- Use root [../../scripts/inspect_model_recipe.py](../../scripts/inspect_model_recipe.py) to print known recipes from bundled root data [../../scripts/model_recipes.json](../../scripts/model_recipes.json).
- Adapt [scripts/model_args_block.sh](scripts/model_args_block.sh) as a project-local shell block.

## Handoff

Use the selected `MODEL_ARGS` in:

- `slime-checkpoint-conversion` for HF to Megatron conversion.
- `slime-rl-training` and `slime-sft-training` for training launch.
