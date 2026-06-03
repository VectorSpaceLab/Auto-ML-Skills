#!/usr/bin/env bash
# AMD/ROCm runtime environment template for slime jobs.
export HIP_VISIBLE_DEVICES="${HIP_VISIBLE_DEVICES:-0,1,2,3,4,5,6,7}"
export PYTORCH_HIP_ALLOC_CONF="${PYTORCH_HIP_ALLOC_CONF:-expandable_segments:True}"
export PYTHONUNBUFFERED=1

AMD_ARGS=(
  --no-gradient-accumulation-fusion
)
