#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import yaml_scalar


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a LLaMA-Factory v1 dataset_info.yaml.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", default="train")
    parser.add_argument("--path", required=True)
    parser.add_argument("--source", default="local")
    parser.add_argument("--converter", choices=["alpaca", "sharegpt", "pair"], default=None)
    parser.add_argument("--split", default=None)
    parser.add_argument("--size", type=int, default=None)
    parser.add_argument("--weight", type=float, default=None)
    args = parser.parse_args()
    lines = [f"{args.name}:", f"  path: {yaml_scalar(args.path)}", f"  source: {yaml_scalar(args.source)}"]
    for key in ["converter", "split", "size", "weight"]:
        value = getattr(args, key)
        if value is not None:
            lines.append(f"  {key}: {yaml_scalar(value)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
