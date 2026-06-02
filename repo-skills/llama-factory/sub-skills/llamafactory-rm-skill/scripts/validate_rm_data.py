#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--format", choices=["v1-pair", "converted-pair"], default="v1-pair")
    args = parser.parse_args()
    rows = records(args.data)
    errors = []
    for idx, row in enumerate(rows):
        keys = ("chosen", "rejected") if args.format == "v1-pair" else ("chosen_messages", "rejected_messages")
        for key in keys:
            if not isinstance(row.get(key), list) or not row.get(key):
                errors.append(f"row {idx}: {key} must be non-empty list")
                continue
            for msg_idx, message in enumerate(row[key]):
                if not isinstance(message, dict):
                    errors.append(f"row {idx}: {key}[{msg_idx}] must be an object")
                    continue
                role = message.get("role")
                content = message.get("content")
                if args.format == "v1-pair" and role not in {"system", "user", "assistant", "tool"}:
                    errors.append(f"row {idx}: {key}[{msg_idx}].role must be OpenAI-style role")
                if args.format == "v1-pair" and not isinstance(content, str):
                    errors.append(f"row {idx}: {key}[{msg_idx}].content must be a string")
        if len(errors) >= 20:
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
