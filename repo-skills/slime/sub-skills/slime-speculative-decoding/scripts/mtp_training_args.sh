#!/usr/bin/env bash
# Online MTP training args for slime. The torch-dist checkpoint must include MTP weights.

MTP_TRAINING_ARGS=(
  --mtp-num-layers 1
  --enable-mtp-training
  --mtp-loss-scaling-factor 0.2
)
