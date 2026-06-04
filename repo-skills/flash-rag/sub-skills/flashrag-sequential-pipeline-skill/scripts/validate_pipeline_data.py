#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def iter_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    if not args.data.is_file():
        print(f"missing data: {args.data}")
        return 1
    rows = iter_rows(args.data)
    errors: list[str] = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {idx}: must be object")
            continue
        question = row.get("question")
        answers = row.get("golden_answers")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"row {idx}: question must be a non-empty string")
        if not isinstance(answers, list) or not answers or not all(isinstance(x, str) and x for x in answers):
            errors.append(f"row {idx}: golden_answers must be a non-empty list of strings")
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
