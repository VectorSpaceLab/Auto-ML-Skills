#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--format", choices=["sharegpt-ranking", "v1-pair"], default="sharegpt-ranking")
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()
    rows = load_records(args.data)
    errors: list[str] = []
    for idx, row in enumerate(rows):
        if args.format == "sharegpt-ranking":
            if not isinstance(row.get("conversations"), list) or not row["conversations"]:
                errors.append(f"row {idx}: conversations must be non-empty list")
            for key in ["chosen", "rejected"]:
                item = row.get(key)
                if not isinstance(item, dict) or not isinstance(item.get("value"), str) or not item.get("value"):
                    errors.append(f"row {idx}: {key} must be a message dict with non-empty value")
        else:
            for key in ["chosen_messages", "rejected_messages"]:
                item = row.get(key)
                if not isinstance(item, list) or not item:
                    errors.append(f"row {idx}: {key} must be non-empty list")
        if len(errors) >= args.max_errors:
            break
    print(f"records: {len(rows)}")
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
