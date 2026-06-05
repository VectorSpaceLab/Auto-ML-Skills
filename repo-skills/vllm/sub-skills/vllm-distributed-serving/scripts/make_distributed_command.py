#!/usr/bin/env python3
"""Generate a vLLM distributed serve command."""

from __future__ import annotations

import argparse
import shlex


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--pipeline-parallel-size", type=int, default=1)
    parser.add_argument("--data-parallel-size", type=int, default=None)
    parser.add_argument("--backend", choices=["ray", "mp", "uni", "external_launcher"], default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    cmd = ["vllm", "serve", args.model, "--host", args.host, "--port", str(args.port)]
    cmd += ["--tensor-parallel-size", str(args.tensor_parallel_size)]
    cmd += ["--pipeline-parallel-size", str(args.pipeline_parallel_size)]
    if args.data_parallel_size:
        cmd += ["--data-parallel-size", str(args.data_parallel_size)]
    if args.backend:
        cmd += ["--distributed-executor-backend", args.backend]
    print(" ".join(shlex.quote(part) for part in cmd))


if __name__ == "__main__":
    main()
