#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--text-key", default="text")
    args = parser.parse_args()
    rows = records(args.data)
    errors = []
    for idx, row in enumerate(rows[:50]):
        if not isinstance(row.get(args.text_key), str) or not row.get(args.text_key).strip():
            errors.append(f"row {idx}: missing non-empty {args.text_key!r}")
    print(f"records: {len(rows)}")
    if errors:
        print("valid: false")
        for error in errors[:20]:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
