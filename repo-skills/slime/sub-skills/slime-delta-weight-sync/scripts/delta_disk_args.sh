#!/usr/bin/env bash
DELTA_ARGS=(
  --update-weight-mode delta
  --update-weight-transport disk
  --update-weight-encoding deltas_zstd
  --update-weight-delta-dir "${DELTA_DIR:-/shared/fs/delta-updates}"
)
