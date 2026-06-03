#!/usr/bin/env python3
"""Emit LLaMA-Factory performance-tuning YAML snippets."""

from __future__ import annotations

import argparse


SNIPPETS = {
    "dynamic-batching": [
        "### batching",
        "enable_dynamic_batching: true",
        "cutoff_len: 2048",
        "dataloader_num_workers: 4",
    ],
    "padding-free": [
        "### padding-free",
        "padding_free: true",
        "flash_attn: fa2",
    ],
    "liger": [
        "### liger kernel",
        "enable_liger_kernel: true",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a LLaMA-Factory performance config snippet.")
    parser.add_argument("--feature", choices=["dynamic-batching", "padding-free", "liger", "ulysses"], required=True)
    parser.add_argument("--context-parallel-size", type=int, default=2)
    args = parser.parse_args()
    if args.feature == "ulysses":
        lines = [
            "### ulysses context parallel",
            f"ulysses_sequence_parallel_size: {args.context_parallel_size}",
            "flash_attn: fa2",
        ]
    else:
        lines = SNIPPETS[args.feature]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
