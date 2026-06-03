#!/usr/bin/env bash
# SGLang speculative decoding args for slime rollout engines.
# Append "${SPECULATIVE_SGLANG_ARGS[@]}" to the slime training command after validating support.

SPECULATIVE_SGLANG_ARGS=(
  --sglang-speculative-algorithm EAGLE
  --sglang-speculative-num-steps 3
  --sglang-speculative-eagle-topk 1
  --sglang-speculative-num-draft-tokens 4
)
