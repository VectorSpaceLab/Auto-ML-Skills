#!/usr/bin/env bash
TIS_ARGS=(
  --use-tis
  --tis-clip "${TIS_CLIP:-2.0}"
  --tis-clip-low "${TIS_CLIP_LOW:-0.0}"
  --get-mismatch-metrics
)
