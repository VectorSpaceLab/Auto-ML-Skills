#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    args = parser.parse_args()
    if not args.data.is_file():
        print(f"missing data: {args.data}")
        return 1
    rows = [json.loads(line) for line in args.data.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = []
    for idx, row in enumerate(rows):
        if not isinstance(row.get("question"), str) or not row["question"].strip():
            errors.append(f"row {idx}: question must be a non-empty string")
        if "golden_answers" in row and not isinstance(row["golden_answers"], list):
            errors.append(f"row {idx}: golden_answers must be a list")
    print(f"records: {len(rows)}")
    if rows:
        print(f"first_question: {rows[0].get('question')}")
    if errors:
        print("valid: false")
        for error in errors[:20]:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
