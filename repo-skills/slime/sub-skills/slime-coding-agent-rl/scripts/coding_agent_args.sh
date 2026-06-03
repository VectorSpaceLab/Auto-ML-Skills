#!/usr/bin/env bash
# Template args for slime coding-agent RL rollouts. Replace module paths and data paths.

CODING_AGENT_ROLLOUT_ARGS=(
  --custom-generate-function-path your_package.coding_agent.generate
  --prompt-data "${PROMPT_DATA:?set PROMPT_DATA}"
  --input-key prompt
  --label-key label
  --metadata-key metadata
  --rollout-batch-size "${ROLLOUT_BATCH_SIZE:-1}"
  --n-samples-per-prompt "${N_SAMPLES_PER_PROMPT:-1}"
  --rollout-max-context-len "${ROLLOUT_MAX_CONTEXT_LEN:-96000}"
  --rollout-max-response-len "${ROLLOUT_MAX_RESPONSE_LEN:-32768}"
  --save-debug-rollout-data "${RUN_ROOT:-runs/coding_agent}/rollout_dumps/rollout_{rollout_id}.pt"
)

CODING_AGENT_SGLANG_ARGS=(
  --sglang-tool-call-parser "${SGLANG_TOOL_CALL_PARSER:-qwen3_coder}"
  --sglang-reasoning-parser "${SGLANG_REASONING_PARSER:-qwen3}"
)
