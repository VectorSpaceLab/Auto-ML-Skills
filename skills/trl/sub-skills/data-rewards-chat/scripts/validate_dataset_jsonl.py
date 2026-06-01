#!/usr/bin/env python
"""Validate JSONL rows against common TRL dataset schemas.

This is a lightweight shape check for local JSONL files. It does not download
datasets, tokenize text, or validate semantic quality.

Examples:
    python scripts/validate_dataset_jsonl.py train.jsonl --type preference
    python scripts/validate_dataset_jsonl.py train.jsonl --type auto --max-rows 100
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMAS = {
    "language-modeling": [{"text"}, {"messages"}],
    "prompt-only": [{"prompt"}],
    "prompt-completion": [{"prompt", "completion"}],
    "preference": [{"chosen", "rejected"}, {"prompt", "chosen", "rejected"}],
    "unpaired-preference": [{"prompt", "completion", "label"}],
    "stepwise": [{"prompt", "completions", "labels"}],
}


def is_messages(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, dict) and "role" in item for item in value)


def classify(row: dict[str, Any]) -> list[str]:
    keys = set(row)
    matches = []
    for name, alternatives in SCHEMAS.items():
        if any(required <= keys for required in alternatives):
            matches.append(name)
    return matches


def validate_row(row: dict[str, Any], expected_type: str) -> list[str]:
    errors = []
    matches = classify(row)
    if expected_type != "auto" and expected_type not in matches:
        required = " or ".join(str(sorted(s)) for s in SCHEMAS[expected_type])
        errors.append(f"does not match {expected_type}; expected columns {required}")

    for key in ["messages", "prompt", "completion", "chosen", "rejected"]:
        value = row.get(key)
        if isinstance(value, list) and value and isinstance(value[0], dict) and not is_messages(value):
            errors.append(f"{key} looks like messages but lacks role keys")
    if "label" in row and not isinstance(row["label"], bool):
        errors.append("label should be boolean for unpaired preference rows")
    if "completions" in row and "labels" in row and len(row["completions"]) != len(row["labels"]):
        errors.append("completions and labels lengths differ")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--type", choices=["auto", *SCHEMAS], default="auto")
    parser.add_argument("--max-rows", type=int, default=1000)
    args = parser.parse_args()

    errors_found = 0
    type_counts: dict[str, int] = {}
    with args.path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, start=1):
            if index > args.max_rows:
                break
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"line {index}: invalid JSON: {exc}")
                errors_found += 1
                continue
            if not isinstance(row, dict):
                print(f"line {index}: row is not an object")
                errors_found += 1
                continue
            matches = classify(row)
            for match in matches or ["unknown"]:
                type_counts[match] = type_counts.get(match, 0) + 1
            for error in validate_row(row, args.type):
                print(f"line {index}: {error}")
                errors_found += 1

    print("type counts:", type_counts)
    if errors_found:
        print(f"errors: {errors_found}")
        return 1
    print("validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
