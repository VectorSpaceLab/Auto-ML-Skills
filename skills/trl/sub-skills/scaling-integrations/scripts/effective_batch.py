#!/usr/bin/env python
"""Compute effective batch size for TRL/Transformers training.

Examples:
    python scripts/effective_batch.py --per-device 4 --devices 8 --grad-accum 2
    python scripts/effective_batch.py --target 128 --devices 8 --per-device 4
"""

from __future__ import annotations

import argparse
import math


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-device", type=int, required=True, help="per_device_train_batch_size.")
    parser.add_argument("--devices", type=int, default=1, help="Number of training devices/processes.")
    parser.add_argument("--grad-accum", type=int, default=None, help="gradient_accumulation_steps.")
    parser.add_argument("--target", type=int, default=None, help="Optional target effective batch size.")
    args = parser.parse_args()

    if args.grad_accum is None:
        if args.target is None:
            parser.error("--grad-accum is required unless --target is provided")
        denominator = args.per_device * args.devices
        grad_accum = max(1, math.ceil(args.target / denominator))
    else:
        grad_accum = args.grad_accum

    effective = args.per_device * args.devices * grad_accum
    print(f"per_device_train_batch_size: {args.per_device}")
    print(f"num_devices: {args.devices}")
    print(f"gradient_accumulation_steps: {grad_accum}")
    print(f"effective_batch_size: {effective}")
    if args.target is not None and effective != args.target:
        print(f"target_effective_batch_size: {args.target}")
        print("note: exact target is not reachable with integer gradient accumulation for these inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
