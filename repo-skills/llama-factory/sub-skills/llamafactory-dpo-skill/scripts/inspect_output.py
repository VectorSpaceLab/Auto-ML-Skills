#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import inspect_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--adapter", action="store_true")
    args = parser.parse_args()
    return inspect_output(args.output_dir, args.adapter)


if __name__ == "__main__":
    raise SystemExit(main())
