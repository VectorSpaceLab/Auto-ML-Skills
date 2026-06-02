#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                yield line_no, {"__json_error__": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    if not args.corpus.is_file():
        print(f"missing corpus: {args.corpus}")
        return 1
    if args.corpus.suffix not in {".jsonl", ".parquet"}:
        print("valid: false")
        print("- corpus must be .jsonl or .parquet for FlashRAG retrieval utilities")
        return 1
    if args.corpus.suffix == ".parquet":
        print("records: unknown without loading parquet")
        print("valid: true")
        return 0

    records = 0
    errors: list[str] = []
    first: dict[str, Any] | None = None
    for line_no, row in iter_jsonl(args.corpus):
        records += 1
        if first is None and "__json_error__" not in row:
            first = row
        if "__json_error__" in row:
            errors.append(f"line {line_no}: invalid JSON: {row['__json_error__']}")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_no}: row must be an object")
            continue
        if "id" not in row:
            errors.append(f"line {line_no}: missing id")
        contents = row.get("contents")
        if not isinstance(contents, str) or not contents.strip():
            errors.append(f"line {line_no}: contents must be a non-empty string")
        if len(errors) >= args.max_errors:
            break

    print(f"records: {records}")
    if first:
        print(f"first_id: {first.get('id')}")
        print(f"first_contents_preview: {first.get('contents', '')[:160].replace(chr(10), ' ')}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
