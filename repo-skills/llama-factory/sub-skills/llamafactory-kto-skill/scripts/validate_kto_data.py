#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import load_records


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LLaMA-Factory KTO data.")
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--format", choices=["sharegpt-kto", "alpaca-kto"], default="sharegpt-kto")
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    rows = load_records(args.data)
    errors: list[str] = []
    positive = 0
    negative = 0
    for idx, row in enumerate(rows):
        label = row.get("label")
        if not isinstance(label, bool):
            errors.append(f"row {idx}: label must be true/false bool")
        elif label:
            positive += 1
        else:
            negative += 1

        if args.format == "sharegpt-kto":
            messages = row.get("messages")
            if not isinstance(messages, list) or len(messages) < 2:
                errors.append(f"row {idx}: messages must contain at least user and assistant turns")
            else:
                expected_roles = ("user", "assistant")
                for turn_idx, message in enumerate(messages):
                    if not isinstance(message, dict):
                        errors.append(f"row {idx}: messages[{turn_idx}] must be an object")
                        continue
                    role = message.get("role")
                    content = _text(message.get("content"))
                    if role != expected_roles[turn_idx % 2]:
                        errors.append(
                            f"row {idx}: messages[{turn_idx}].role must alternate user/assistant, got {role!r}"
                        )
                    if not content:
                        errors.append(f"row {idx}: messages[{turn_idx}].content must be non-empty string")
        else:
            if not _text(row.get("instruction")):
                errors.append(f"row {idx}: instruction must be non-empty string")
            if not _text(row.get("output")):
                errors.append(f"row {idx}: output must be non-empty string")

        if len(errors) >= args.max_errors:
            break

    print(f"records: {len(rows)}")
    print(f"format: {args.format}")
    print(f"label_true: {positive}")
    print(f"label_false: {negative}")
    if positive == 0 or negative == 0:
        errors.append("KTO should include both desirable label=true and undesirable label=false examples")
    if errors:
        print("valid: false")
        for error in errors[: args.max_errors]:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
