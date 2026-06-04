#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    if not args.data.is_file():
        print(f"missing data: {args.data}")
        return 1
    if args.data.suffix == ".parquet":
        print("format: parquet")
        print("valid: true")
        print("note: parquet schema will be checked by FlashRAG/datasets at runtime")
        return 0

    rows = load_json_rows(args.data)
    errors: list[str] = []
    image_count = 0
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {idx}: must be object")
            continue
        question = row.get("question") or row.get("text")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"row {idx}: question or text must be a non-empty string")
        if row.get("image") not in [None, ""]:
            image_count += 1
        answers = row.get("golden_answers", row.get("answers", []))
        if answers and not isinstance(answers, list):
            errors.append(f"row {idx}: golden_answers/answers must be a list when present")
        if len(errors) >= args.max_errors:
            break

    print(f"records: {len(rows)}")
    print(f"records_with_image: {image_count}")
    if rows:
        print(f"first_question: {rows[0].get('question') or rows[0].get('text')}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
