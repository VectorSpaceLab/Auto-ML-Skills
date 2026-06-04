#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def iter_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()
    rows = iter_rows(args.data)
    errors: list[str] = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {idx}: must be object")
            continue
        if not isinstance(row.get("question"), str) or not row.get("question", "").strip():
            errors.append(f"row {idx}: missing non-empty question")
        answers = row.get("golden_answers")
        if not isinstance(answers, list) or not answers or not all(isinstance(x, str) and x for x in answers):
            errors.append(f"row {idx}: golden_answers must be a non-empty list of strings")
        if len(errors) >= args.max_errors:
            break
    print(f"records: {len(rows)}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
