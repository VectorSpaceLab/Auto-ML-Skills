#!/usr/bin/env bash
FULLY_ASYNC_ARGS=(
  --rollout-function-path slime.rollout.fully_async_rollout.generate_rollout_fully_async
  --sglang-server-concurrency "${SGLANG_SERVER_CONCURRENCY:-512}"
)
