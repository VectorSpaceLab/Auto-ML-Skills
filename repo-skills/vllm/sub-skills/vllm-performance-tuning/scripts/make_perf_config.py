#!/usr/bin/env python3
"""Create a vLLM serve config with selected performance flags."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-model-len", type=int, default=2048)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.9)
    parser.add_argument("--enable-prefix-caching", action="store_true")
    parser.add_argument("--quantization", default=None)
    args = parser.parse_args()
    lines = [
        f"model: {args.model}",
        "host: \"127.0.0.1\"",
        "port: 8000",
        "dtype: auto",
        "generation-config: vllm",
        f"max-model-len: {args.max_model_len}",
        f"gpu-memory-utilization: {args.gpu_memory_utilization}",
    ]
    if args.enable_prefix_caching:
        lines.append("enable-prefix-caching: true")
    if args.quantization:
        lines.append(f"quantization: {args.quantization}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
