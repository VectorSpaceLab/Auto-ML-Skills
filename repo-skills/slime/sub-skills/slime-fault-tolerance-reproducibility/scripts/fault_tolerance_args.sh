#!/usr/bin/env bash
FAULT_TOLERANCE_ARGS=(
  --use-fault-tolerance
  --rollout-health-check-first-wait "${ROLLOUT_HEALTH_CHECK_FIRST_WAIT:-600}"
  --rollout-health-check-interval "${ROLLOUT_HEALTH_CHECK_INTERVAL:-10}"
  --rollout-health-check-timeout "${ROLLOUT_HEALTH_CHECK_TIMEOUT:-5}"
)
