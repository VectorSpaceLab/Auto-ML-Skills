#!/usr/bin/env python3
"""Write a minimal vLLM serve YAML config."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--out", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--dtype", default="auto")
    parser.add_argument("--max-model-len", type=int, default=2048)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.9)
    parser.add_argument("--enable-lora", action="store_true")
    args = parser.parse_args()
    lines = [
        f"model: {args.model}",
        f'host: "{args.host}"',
        f"port: {args.port}",
        f"dtype: {args.dtype}",
        "generation-config: vllm",
        f"max-model-len: {args.max_model_len}",
        f"tensor-parallel-size: {args.tensor_parallel_size}",
        f"gpu-memory-utilization: {args.gpu_memory_utilization}",
    ]
    if args.enable_lora:
        lines.append("enable-lora: true")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
