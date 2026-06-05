#!/usr/bin/env python3
"""Rough KV cache memory estimator for planning."""

from __future__ import annotations

import argparse


DTYPE_BYTES = {"fp8": 1, "float8": 1, "float16": 2, "bfloat16": 2, "float32": 4}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layers", type=int, required=True)
    parser.add_argument("--hidden-size", type=int, required=True)
    parser.add_argument("--tokens", type=int, required=True)
    parser.add_argument("--dtype", choices=sorted(DTYPE_BYTES), default="float16")
    parser.add_argument("--replicas", type=int, default=1)
    args = parser.parse_args()
    bytes_total = 2 * args.layers * args.hidden_size * args.tokens * DTYPE_BYTES[args.dtype] * args.replicas
    gib = bytes_total / (1024 ** 3)
    print(f"estimated_kv_cache_gib={gib:.3f}")
    print("This is a rough planning estimate; real vLLM allocation depends on architecture, block size, parallelism, and backend.")


if __name__ == "__main__":
    main()
