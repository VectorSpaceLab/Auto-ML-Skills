#!/usr/bin/env bash
# Template: export a Megatron torch_dist iteration back to Hugging Face format.
set -euo pipefail

: "${MEGATRON_PATH:?Set MEGATRON_PATH to a full Megatron-LM checkout}"
: "${MEGATRON_ITER_DIR:?Set MEGATRON_ITER_DIR to a checkpoint iteration directory}"
: "${HF_OUTPUT:?Set HF_OUTPUT to the export directory}"
: "${ORIGIN_HF:?Set ORIGIN_HF to the original Hugging Face checkpoint}"

SKILL_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"

PYTHONPATH="${MEGATRON_PATH}:${PYTHONPATH:-}" python "${SKILL_ROOT}/scripts/convert_torch_dist_to_hf.py" \
  --input-dir "${MEGATRON_ITER_DIR}" \
  --output-dir "${HF_OUTPUT}" \
  --origin-hf-dir "${ORIGIN_HF}" \
  --force
