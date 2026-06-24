# Checkpoint Conversion Workflows

## HF To Megatron `torch_dist`

Megatron cannot directly train from a Hugging Face checkpoint. Convert first:

```bash
export MEGATRON_PATH=/path/to/Megatron-LM
export HF_CHECKPOINT=/models/Qwen3-0.6B
export MEGATRON_SAVE=/models/Qwen3-0.6B_torch_dist

MODEL_ARGS=( $(python /path/to/skill/slime/scripts/inspect_model_recipe.py qwen3-0.6b) )

PYTHONPATH="${MEGATRON_PATH}:${PYTHONPATH}" python /path/to/skill/slime/scripts/convert_hf_to_torch_dist.py \
  "${MODEL_ARGS[@]}" \
  --hf-checkpoint "${HF_CHECKPOINT}" \
  --save "${MEGATRON_SAVE}"
```

The bundled runner uses the installed `slime` package and a full Megatron-LM checkout on `PYTHONPATH`; it does not require the original inspected source checkout.

## Megatron `torch_dist` To HF

Use an iteration directory as input:

```bash
PYTHONPATH="${MEGATRON_PATH}:${PYTHONPATH}" python /path/to/skill/slime/scripts/convert_torch_dist_to_hf.py \
  --input-dir /checkpoints/model_slime/iter_0000100 \
  --output-dir /exports/model_iter_100_hf \
  --origin-hf-dir /models/Qwen3-0.6B \
  --force
```

If the output embedding looks wrong, specify `--vocab-size` matching the model recipe.

## Checkpoint Layout

Megatron checkpoint root:

```text
model_slime/
  latest_checkpointed_iteration.txt
  iter_0000001/
    *.distcp
```

Use the root for `--load`, `--save`, and `--ref-load`. Use an iteration directory for HF export tools.

## Resume Pattern

For resume:

```bash
--load /checkpoints/model_slime
--save /checkpoints/model_slime
```

If `--load` is empty or invalid, slime initializes actor weights from `--ref-load`.
