#!/usr/bin/env bash
# Template for launching a slime training job through Ray.
#
# Copy this into a project run directory and edit the path variables and args
# blocks. It intentionally does not kill existing processes; do that manually
# only when you know no other Ray jobs are using the node.
set -euo pipefail

: "${NUM_GPUS:=8}"
: "${MASTER_ADDR:=127.0.0.1}"
: "${MEGATRON_PATH:?Set MEGATRON_PATH to a full Megatron-LM checkout}"
: "${SLIME_RUNNER:?Set SLIME_RUNNER to run_slime_train.py or run_slime_train_async.py}"

export PYTHONUNBUFFERED=1
export no_proxy="127.0.0.1,${MASTER_ADDR},${no_proxy:-}"
# Ray creates Unix-domain sockets under its temp directory. Keep this path
# short; long nested temp paths can exceed the 107-byte AF_UNIX socket limit.
export RAY_TMPDIR="${RAY_TMPDIR:-/tmp/ray}"
mkdir -p "${RAY_TMPDIR}"

TORCH_LD_LIBRARY_PATH=$(python - <<'PY'
from pathlib import Path
import torch

site = Path(torch.__file__).resolve().parents[1]
candidates = [
    site / "torch" / "lib",
    site / "nvidia" / "cuda_runtime" / "lib",
    site / "nvidia" / "cuda_nvrtc" / "lib",
    site / "nvidia" / "cublas" / "lib",
    site / "nvidia" / "cudnn" / "lib",
    site / "nvidia" / "nccl" / "lib",
    site / "nvidia" / "nvtx" / "lib",
]
print(":".join(str(path) for path in candidates if path.exists()))
PY
)
if [[ -n "${TORCH_LD_LIBRARY_PATH}" ]]; then
  export LD_LIBRARY_PATH="${TORCH_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH:-}"
fi

ray start --head \
  --node-ip-address "${MASTER_ADDR}" \
  --num-gpus "${NUM_GPUS}" \
  --disable-usage-stats \
  --dashboard-host=0.0.0.0 \
  --dashboard-port=8265

RUNTIME_ENV_JSON=$(cat <<JSON
{
  "env_vars": {
    "PYTHONPATH": "${MEGATRON_PATH}",
    "LD_LIBRARY_PATH": "${LD_LIBRARY_PATH:-}",
    "CUDA_DEVICE_MAX_CONNECTIONS": "1",
    "PYTHONUNBUFFERED": "1"
  }
}
JSON
)

ray job submit --address="http://127.0.0.1:8265" \
  --runtime-env-json="${RUNTIME_ENV_JSON}" \
  -- python "${SLIME_RUNNER}" "$@"
