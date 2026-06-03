#!/usr/bin/env bash
VLM_ARGS=(
  --multimodal-keys '{"image":"images"}'
  --input-key "${INPUT_KEY:-messages}"
  --label-key "${LABEL_KEY:-answer}"
  --apply-chat-template
)
