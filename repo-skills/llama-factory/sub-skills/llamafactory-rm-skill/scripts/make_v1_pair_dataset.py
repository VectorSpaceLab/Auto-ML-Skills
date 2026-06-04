#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import scalar


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", default="rm_train")
    parser.add_argument("--path", required=True)
    parser.add_argument("--source", default="local")
    parser.add_argument("--converter", choices=["pair"], default=None)
    args = parser.parse_args()
    lines = [f"{args.name}:", f"  path: {scalar(args.path)}", f"  source: {scalar(args.source)}"]
    if args.converter:
        lines.append(f"  converter: {args.converter}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
