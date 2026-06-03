#!/usr/bin/env bash
LOW_PRECISION_TRAINING_ARGS=(
  --fp8-format e4m3
  --fp8-recipe blockwise
)
