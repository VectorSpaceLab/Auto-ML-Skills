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
    errors: list[str] = []
    rows = []
    with args.data.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            rows.append(row)
            if not isinstance(row.get("question"), str) or not row["question"].strip():
                errors.append(f"line {line_no}: question must be a non-empty string")
            answers = row.get("golden_answers")
            if not isinstance(answers, list) or not answers or not all(isinstance(x, str) and x for x in answers):
                errors.append(f"line {line_no}: golden_answers must be a non-empty list of strings")
            if len(errors) >= args.max_errors:
                break
    print(f"records: {len(rows)}")
    if rows:
        print(f"first_question: {rows[0].get('question')}")
        print(f"first_answer: {(rows[0].get('golden_answers') or [''])[0]}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
