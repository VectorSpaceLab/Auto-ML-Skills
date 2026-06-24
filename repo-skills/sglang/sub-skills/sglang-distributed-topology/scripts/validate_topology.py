#!/usr/bin/env python3
"""Validate obvious SGLang topology mistakes."""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SGLang distributed topology arithmetic and URLs.")
    parser.add_argument("--gpus-per-node", type=int, default=1)
    parser.add_argument("--nnodes", type=int, default=1)
    parser.add_argument("--tp-size", type=int, default=1)
    parser.add_argument("--dp-size", type=int, default=1)
    parser.add_argument("--pp-size", type=int, default=1)
    parser.add_argument("--worker-url", action="append", default=[])
    parser.add_argument("--prefill", action="append", default=[], help="Prefill URL, optionally URL:BOOTSTRAP_PORT in notes.")
    parser.add_argument("--decode", action="append", default=[])
    args = parser.parse_args()

    total_gpus = args.gpus_per_node * args.nnodes
    required = args.tp_size * args.dp_size * args.pp_size
    issues = []
    if min(args.gpus_per_node, args.nnodes, args.tp_size, args.dp_size, args.pp_size) < 1:
        issues.append("all size arguments must be >= 1")
    if required > total_gpus:
        issues.append(f"tp*dp*pp={required} exceeds visible GPUs={total_gpus}")
    if args.prefill or args.decode:
        if not args.prefill or not args.decode:
            issues.append("PD disaggregation needs both --prefill and --decode endpoints")
    for field, urls in [("worker_url", args.worker_url), ("prefill", args.prefill), ("decode", args.decode)]:
        for url in urls:
            if not (url.startswith("http://") or url.startswith("https://")):
                issues.append(f"{field} does not look like an HTTP URL: {url}")

    report = {"total_gpus": total_gpus, "required_parallel_ranks": required, "issues": issues}
    print(json.dumps(report, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
