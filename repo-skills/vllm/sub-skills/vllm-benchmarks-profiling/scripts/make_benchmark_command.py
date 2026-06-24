#!/usr/bin/env python3
"""Generate a vLLM benchmark command."""

from __future__ import annotations

import argparse
import shlex


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=["latency", "throughput", "serve", "startup", "mm-processor"], default="throughput")
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--backend", default="vllm")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--num-prompts", type=int, default=8)
    parser.add_argument("--out", default=None, help="Optional JSON output path.")
    args = parser.parse_args()
    cmd = ["vllm", "bench", args.kind]
    if args.kind == "serve":
        cmd += ["--backend", args.backend, "--model", args.model, "--base-url", args.base_url, "--num-prompts", str(args.num_prompts)]
    else:
        cmd += ["--model", args.model, "--num-prompts", str(args.num_prompts)]
    if args.out:
        cmd += ["--save-result", "--result-filename", args.out]
    print(" ".join(shlex.quote(part) for part in cmd))


if __name__ == "__main__":
    main()
