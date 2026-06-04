#!/usr/bin/env bash
DEBUG_ROLLOUT_ARGS=(
  --debug-rollout-only
  --save-debug-rollout-data "${DEBUG_ROLLOUT_PATH:-/tmp/slime_rollout_{rollout_id}.pt}"
)

DEBUG_TRAIN_ARGS=(
  --debug-train-only
  --load-debug-rollout-data "${DEBUG_ROLLOUT_PATH:-/tmp/slime_rollout_{rollout_id}.pt}"
)
