#!/usr/bin/env bash
# Start a local Ray head for slime jobs.
set -euo pipefail

: "${NUM_GPUS:=8}"
: "${MASTER_ADDR:=127.0.0.1}"

export no_proxy="127.0.0.1,${MASTER_ADDR},${no_proxy:-}"

ray start --head \
  --node-ip-address "${MASTER_ADDR}" \
  --num-gpus "${NUM_GPUS}" \
  --disable-usage-stats \
  --dashboard-host=0.0.0.0 \
  --dashboard-port="${RAY_DASHBOARD_PORT:-8265}"
