#!/usr/bin/env bash
# Template: convert a Hugging Face checkpoint to Megatron torch_dist for slime.
set -euo pipefail

: "${MEGATRON_PATH:?Set MEGATRON_PATH to a full Megatron-LM checkout}"
: "${HF_CHECKPOINT:?Set HF_CHECKPOINT to the local HF model directory}"
: "${MEGATRON_SAVE:?Set MEGATRON_SAVE to the output torch_dist directory}"
: "${MODEL_RECIPE:=qwen3-0.6b}"

SKILL_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
MODEL_ARGS=( $(python "${SKILL_ROOT}/scripts/inspect_model_recipe.py" "${MODEL_RECIPE}") )

PYTHONPATH="${MEGATRON_PATH}:${PYTHONPATH:-}" python "${SKILL_ROOT}/scripts/convert_hf_to_torch_dist.py" \
  "${MODEL_ARGS[@]}" \
  --hf-checkpoint "${HF_CHECKPOINT}" \
  --save "${MEGATRON_SAVE}"
