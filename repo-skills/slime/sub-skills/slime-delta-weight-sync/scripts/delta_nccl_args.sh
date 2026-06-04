#!/usr/bin/env bash
DELTA_ARGS=(
  --update-weight-mode delta
  --update-weight-transport nccl
  --update-weight-encoding indices
)
