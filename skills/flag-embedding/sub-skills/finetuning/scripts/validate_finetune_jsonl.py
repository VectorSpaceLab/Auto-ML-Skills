#!/usr/bin/env python3
"""Validate FlagEmbedding fine-tuning JSONL data.

This script has no FlagEmbedding dependency and performs no model downloads.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_candidate_pool(row: dict[str, Any], line_no: int) -> list[str]:
    errors = []
    if "text" not in row:
        errors.append(f"line {line_no}: missing required field 'text'")
    elif not isinstance(row["text"], str) or not row["text"].strip():
        errors.append(f"line {line_no}: 'text' must be a non-empty string")
    return errors


def validate_train_row(row: dict[str, Any], line_no: int, require_scores: bool) -> list[str]:
    errors: list[str] = []

    if not isinstance(row.get("query"), str) or not row.get("query", "").strip():
        errors.append(f"line {line_no}: 'query' must be a non-empty string")

    for key in ("pos", "neg"):
        value = row.get(key)
        if not isinstance(value, list):
            errors.append(f"line {line_no}: '{key}' must be a list of strings")
            continue
        if key == "pos" and not value:
            errors.append(f"line {line_no}: 'pos' must contain at least one string")
        bad = [idx for idx, item in enumerate(value) if not isinstance(item, str)]
        if bad:
            errors.append(f"line {line_no}: '{key}' contains non-string entries at indexes {bad[:5]}")

    for score_key, text_key in (("pos_scores", "pos"), ("neg_scores", "neg")):
        scores = row.get(score_key)
        texts = row.get(text_key)
        if scores is None:
            if require_scores:
                errors.append(f"line {line_no}: missing '{score_key}' required by --require-scores")
            continue
        if not isinstance(scores, list):
            errors.append(f"line {line_no}: '{score_key}' must be a list of numbers")
            continue
        if isinstance(texts, list) and len(scores) != len(texts):
            errors.append(f"line {line_no}: len({score_key})={len(scores)} does not match len({text_key})={len(texts)}")
        bad_scores = [idx for idx, item in enumerate(scores) if not is_number(item)]
        if bad_scores:
            errors.append(f"line {line_no}: '{score_key}' contains non-numeric entries at indexes {bad_scores[:5]}")

    if "prompt" in row and row["prompt"] is not None and not isinstance(row["prompt"], str):
        errors.append(f"line {line_no}: optional 'prompt' must be a string when present")
    if "type" in row and row["type"] is not None and not isinstance(row["type"], str):
        errors.append(f"line {line_no}: optional 'type' must be a string when present")

    return errors


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                yield line_no, None, [f"line {line_no}: invalid JSON: {exc.msg}"]
                continue
            if not isinstance(row, dict):
                yield line_no, None, [f"line {line_no}: row must be a JSON object"]
                continue
            yield line_no, row, []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="JSONL files to validate.")
    parser.add_argument("--task", choices=["embedder", "reranker"], default="embedder", help="Task label for the report.")
    parser.add_argument("--require-scores", action="store_true", help="Require pos_scores and neg_scores.")
    parser.add_argument("--candidate-pool", action="store_true", help="Validate candidate-pool rows with a text field.")
    parser.add_argument("--max-errors", type=int, default=50, help="Stop after this many errors.")
    args = parser.parse_args()

    total_rows = 0
    errors: list[str] = []

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file does not exist")
            continue
        if path.is_dir():
            errors.append(f"{path}: expected a JSONL file, got a directory")
            continue
        for line_no, row, row_errors in iter_jsonl(path):
            if row_errors:
                errors.extend(f"{path}: {err}" for err in row_errors)
            elif row is not None:
                total_rows += 1
                if args.candidate_pool:
                    row_errors = validate_candidate_pool(row, line_no)
                else:
                    row_errors = validate_train_row(row, line_no, args.require_scores)
                errors.extend(f"{path}: {err}" for err in row_errors)
            if len(errors) >= args.max_errors:
                break

    report = {
        "ok": not errors,
        "task": args.task,
        "candidate_pool": args.candidate_pool,
        "rows_checked": total_rows,
        "errors": errors[: args.max_errors],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
