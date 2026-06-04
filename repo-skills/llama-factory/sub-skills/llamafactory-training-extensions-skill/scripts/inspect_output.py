#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import inspect_train_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--adapter", action="store_true")
    args = parser.parse_args()
    rc = inspect_train_output(args.output_dir, adapter=args.adapter)
    profiler = args.output_dir / "profiler"
    if profiler.exists():
        print("profiler:")
        for path in sorted(profiler.rglob("*"))[:20]:
            if path.is_file():
                print(f"- {path}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
