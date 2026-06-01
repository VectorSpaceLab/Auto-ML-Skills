#!/usr/bin/env python
"""Build a starter `trl vllm-serve` command.

The script only prints a command. It does not start a server.

Example:
    python scripts/vllm_server_command.py --model Qwen/Qwen2.5-7B --gpus 0,1,2,3 --tp 4
"""

from __future__ import annotations

import argparse
import shlex


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--gpus", default=None, help="CUDA_VISIBLE_DEVICES value for the server.")
    parser.add_argument("--tp", "--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.9)
    parser.add_argument("--dtype", default="auto")
    parser.add_argument("--max-model-len", type=int, default=None)
    args = parser.parse_args()

    command = []
    if args.gpus:
        command.append(f"CUDA_VISIBLE_DEVICES={shlex.quote(args.gpus)}")
    command.extend(
        [
            "trl",
            "vllm-serve",
            "--model",
            args.model,
            "--tensor-parallel-size",
            str(args.tp),
            "--host",
            args.host,
            "--port",
            str(args.port),
            "--gpu-memory-utilization",
            str(args.gpu_memory_utilization),
            "--dtype",
            args.dtype,
        ]
    )
    if args.max_model_len is not None:
        command.extend(["--max-model-len", str(args.max_model_len)])

    print(" ".join(shlex.quote(part) if i != 0 or not part.startswith("CUDA_VISIBLE_DEVICES=") else part for i, part in enumerate(command)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
