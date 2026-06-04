#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import load_records


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local LLaMA-Factory registered dataset.")
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    info_path = args.dataset_dir / "dataset_info.json"
    if not info_path.is_file():
        raise SystemExit(f"dataset_info.json not found: {info_path}")
    info = json.loads(info_path.read_text(encoding="utf-8"))
    if args.dataset_name not in info:
        raise SystemExit(f"dataset {args.dataset_name!r} is not registered in {info_path}")

    item = info[args.dataset_name]
    data_path = args.dataset_dir / item["file_name"]
    rows = load_records(data_path)
    fmt = item.get("formatting", "alpaca")
    columns = item.get("columns", {})
    tags = item.get("tags", {})
    errors: list[str] = []
    ranking = bool(item.get("ranking"))
    kto_tag = columns.get("kto_tag")
    label_counts = {True: 0, False: 0}

    for idx, row in enumerate(rows):
        if fmt == "alpaca":
            prompt = columns.get("prompt", "instruction")
            response = columns.get("response", "output")
            if not _text(row.get(prompt)):
                errors.append(f"row {idx}: {prompt!r} must be a non-empty string")
            if ranking:
                for key in [columns.get("chosen", "chosen"), columns.get("rejected", "rejected")]:
                    if not _text(row.get(key)):
                        errors.append(f"row {idx}: {key!r} must be a non-empty string for ranking data")
            elif not _text(row.get(response)):
                errors.append(f"row {idx}: {response!r} must be a non-empty string")
        elif fmt in {"sharegpt", "openai"}:
            messages_col = columns.get("messages", "messages" if fmt == "openai" else "conversations")
            role_tag = tags.get("role_tag", "role" if fmt == "openai" else "from")
            content_tag = tags.get("content_tag", "content" if fmt == "openai" else "value")
            messages = row.get(messages_col)
            if not isinstance(messages, list) or len(messages) < 2:
                errors.append(f"row {idx}: {messages_col!r} must contain at least two messages")
            else:
                for turn_idx, message in enumerate(messages):
                    if not isinstance(message, dict):
                        errors.append(f"row {idx}: message {turn_idx} must be an object")
                        continue
                    if not _text(message.get(role_tag)):
                        errors.append(f"row {idx}: message {turn_idx} missing role tag {role_tag!r}")
                    if not _text(message.get(content_tag)):
                        errors.append(f"row {idx}: message {turn_idx} missing content tag {content_tag!r}")
        else:
            errors.append(f"unsupported formatting: {fmt}")

        if kto_tag:
            label = row.get(kto_tag)
            if not isinstance(label, bool):
                errors.append(f"row {idx}: KTO label {kto_tag!r} must be true/false")
            else:
                label_counts[label] += 1

        if len(errors) >= args.max_errors:
            break

    if kto_tag and (label_counts[True] == 0 or label_counts[False] == 0):
        errors.append("KTO data should contain both true and false labels")

    print(f"dataset_dir: {args.dataset_dir.resolve()}")
    print(f"dataset_name: {args.dataset_name}")
    print(f"file: {data_path}")
    print(f"records: {len(rows)}")
    print(f"format: {fmt}")
    print(f"ranking: {str(ranking).lower()}")
    if kto_tag:
        print(f"label_true: {label_counts[True]}")
        print(f"label_false: {label_counts[False]}")
    if errors:
        print("valid: false")
        for error in errors[: args.max_errors]:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
