#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=5)
    args = parser.parse_args()
    errors: list[str] = []
    rows = []
    with args.predictions.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    print(f"rows: {len(rows)}")
    for idx, row in enumerate(rows[: args.max_rows]):
        for key in ["predict", "label"]:
            if key not in row:
                errors.append(f"row {idx} missing {key}")
    if rows:
        print("first_row_keys: " + ",".join(sorted(rows[0].keys())))
    else:
        errors.append("prediction file is empty")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
