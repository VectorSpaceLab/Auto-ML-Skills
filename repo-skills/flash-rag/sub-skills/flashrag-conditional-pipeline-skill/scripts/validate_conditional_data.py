#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()
    if not args.data.is_file():
        print(f"missing data: {args.data}")
        return 1
    rows = [json.loads(line) for line in args.data.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors: list[str] = []
    for idx, row in enumerate(rows):
        if not isinstance(row.get("question"), str) or not row["question"].strip():
            errors.append(f"row {idx}: question must be non-empty string")
        answers = row.get("golden_answers", [])
        if not isinstance(answers, list):
            errors.append(f"row {idx}: golden_answers must be a list")
        if len(errors) >= args.max_errors:
            break
    print(f"records: {len(rows)}")
    if rows:
        print(f"first_question: {rows[0].get('question')}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
