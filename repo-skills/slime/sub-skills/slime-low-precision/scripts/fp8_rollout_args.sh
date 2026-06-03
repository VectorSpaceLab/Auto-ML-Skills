#!/usr/bin/env bash
LOW_PRECISION_ARGS=(
  --hf-checkpoint "${FP8_HF_CHECKPOINT:?Set FP8_HF_CHECKPOINT}"
  --sglang-kv-cache-dtype fp8_e4m3
)
