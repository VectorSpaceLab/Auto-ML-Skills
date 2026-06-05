#!/usr/bin/env python3
"""Create a vLLM serve config with selected performance flags."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-model-len", type=int, default=2048)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.9)
    parser.add_argument("--enable-prefix-caching", action="store_true")
    parser.add_argument("--prefix-caching-hash-algo", default=None)
    parser.add_argument("--quantization", default=None)
    parser.add_argument("--kv-cache-dtype", default=None)
    parser.add_argument("--calculate-kv-scales", action="store_true")
    parser.add_argument("--spec-model", default=None)
    parser.add_argument("--spec-method", default=None)
    parser.add_argument("--spec-tokens", type=int, default=None)
    parser.add_argument("--speculative-config", default=None, help="Raw JSON object for --speculative-config.")
    parser.add_argument("--enable-dbo", action="store_true")
    parser.add_argument("--dbo-decode-token-threshold", type=int, default=None)
    parser.add_argument("--dbo-prefill-token-threshold", type=int, default=None)
    parser.add_argument("--compilation-config", default=None, help="Raw JSON object for --compilation-config.")
    parser.add_argument("--optimization-level", default=None)
    parser.add_argument("--performance-mode", action="store_true")
    parser.add_argument("--enforce-eager", action="store_true", help="Disable CUDA graph/compile capture for diagnosis.")
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
    if args.prefix_caching_hash_algo:
        lines.append(f"prefix-caching-hash-algo: {args.prefix_caching_hash_algo}")
    if args.quantization:
        lines.append(f"quantization: {args.quantization}")
    if args.kv_cache_dtype:
        lines.append(f"kv-cache-dtype: {args.kv_cache_dtype}")
    if args.calculate_kv_scales:
        lines.append("calculate-kv-scales: true")
    if args.speculative_config:
        json.loads(args.speculative_config)
        lines.append(f"speculative-config: '{args.speculative_config}'")
    else:
        if args.spec_model:
            lines.append(f"spec-model: {args.spec_model}")
        if args.spec_method:
            lines.append(f"spec-method: {args.spec_method}")
        if args.spec_tokens is not None:
            lines.append(f"spec-tokens: {args.spec_tokens}")
    if args.enable_dbo:
        lines.append("enable-dbo: true")
    if args.dbo_decode_token_threshold is not None:
        lines.append(f"dbo-decode-token-threshold: {args.dbo_decode_token_threshold}")
    if args.dbo_prefill_token_threshold is not None:
        lines.append(f"dbo-prefill-token-threshold: {args.dbo_prefill_token_threshold}")
    if args.compilation_config:
        json.loads(args.compilation_config)
        lines.append(f"compilation-config: '{args.compilation_config}'")
    if args.optimization_level:
        lines.append(f"optimization-level: {args.optimization_level}")
    if args.performance_mode:
        lines.append("performance-mode: true")
    if args.enforce_eager:
        lines.append("enforce-eager: true")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
