# Using Model Recipes

## Shell Pattern

```bash
MODEL_ARGS=( $(python /path/to/skill/slime/scripts/inspect_model_recipe.py qwen3-0.6b) )

python ... \
  "${MODEL_ARGS[@]}" \
  --hf-checkpoint /models/Qwen3-0.6B \
  ...
```

For structured inspection instead of shell words:

```bash
python /path/to/skill/slime/scripts/inspect_model_recipe.py qwen3-0.6b --json
```

The script reads bundled `scripts/model_recipes.json`; future agents should not fetch model scripts from an original slime checkout for the listed recipes.

## Override Pattern

If a model variant changes RoPE base:

```bash
MODEL_ARGS=( $(python /path/to/skill/slime/scripts/inspect_model_recipe.py qwen3-4b) )
MODEL_ARGS+=(--rotary-base 10000)
```

Avoid duplicating conflicting flags. If a flag already exists in the array, remove or replace it deliberately.

## Conversion And Training Consistency

Use the same model recipe for:

- HF to Megatron conversion.
- RL/SFT training launch.
- Megatron to HF export when a model name or origin HF directory is not enough.

Mismatch between conversion and training recipes can load incorrectly or produce bad generations without obvious shape errors.
