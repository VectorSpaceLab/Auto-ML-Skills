#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import inspect


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    return inspect(args.output_dir)


if __name__ == "__main__":
    raise SystemExit(main())
