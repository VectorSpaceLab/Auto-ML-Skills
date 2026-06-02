#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import load_json_or_jsonl


def text_content(content) -> bool:
    if isinstance(content, str):
        return bool(content)
    if isinstance(content, list):
        return all(isinstance(x, dict) and x.get("type") == "text" and "value" in x for x in content)
    return False


def validate_messages(records: list[dict], max_errors: int) -> list[str]:
    errors: list[str] = []
    for idx, row in enumerate(records):
        messages = row.get("messages")
        if not isinstance(messages, list) or not messages:
            errors.append(f"row {idx}: missing non-empty messages")
            continue
        assistant_loss = False
        for midx, msg in enumerate(messages):
            if msg.get("role") not in {"system", "user", "assistant", "tool"}:
                errors.append(f"row {idx} message {midx}: invalid role")
            if not text_content(msg.get("content")):
                errors.append(f"row {idx} message {midx}: invalid text content")
            if msg.get("role") == "assistant" and float(msg.get("loss_weight", 1.0)) > 0:
                assistant_loss = True
        if not assistant_loss:
            errors.append(f"row {idx}: no assistant message with positive loss_weight")
        if len(errors) >= max_errors:
            break
    return errors


def validate_alpaca(records: list[dict], max_errors: int) -> list[str]:
    errors: list[str] = []
    for idx, row in enumerate(records):
        if not isinstance(row.get("instruction"), str):
            errors.append(f"row {idx}: instruction must be string")
        if not isinstance(row.get("output"), str) or not row.get("output"):
            errors.append(f"row {idx}: output must be non-empty string")
        if len(errors) >= max_errors:
            break
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--format", choices=["messages", "alpaca"], default="messages")
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()
    records = load_json_or_jsonl(args.data)
    errors = validate_messages(records, args.max_errors) if args.format == "messages" else validate_alpaca(records, args.max_errors)
    print(f"records: {len(records)}")
    print(f"format: {args.format}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
