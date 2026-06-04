#!/usr/bin/env bash
EVAL_ARGS=(
  --eval-interval "${EVAL_INTERVAL:-5}"
  --eval-config "${EVAL_CONFIG:?Set EVAL_CONFIG}"
)
