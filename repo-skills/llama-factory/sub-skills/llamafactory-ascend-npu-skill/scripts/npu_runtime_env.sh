#!/usr/bin/env bash
# Template environment for LLaMA-Factory Ascend NPU runs.
# Source or copy these exports before launching accelerate/llamafactory-cli.

export ASCEND_RT_VISIBLE_DEVICES="${ASCEND_RT_VISIBLE_DEVICES:-0}"
export TOKENIZERS_PARALLELISM="${TOKENIZERS_PARALLELISM:-false}"
export PYTORCH_NPU_ALLOC_CONF="${PYTORCH_NPU_ALLOC_CONF:-expandable_segments:True}"
