#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import check_output_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--adapter", action="store_true")
    args = parser.parse_args()
    return check_output_dir(args.output_dir, adapter=args.adapter)


if __name__ == "__main__":
    raise SystemExit(main())
