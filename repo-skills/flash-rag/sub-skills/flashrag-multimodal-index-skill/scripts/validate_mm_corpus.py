#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


TEXT_KEYS = {"contents", "text", "caption", "question"}
IMAGE_KEYS = {"image", "image_path", "image_url", "image_id"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    args = parser.parse_args()
    errors: list[str] = []
    rows = []
    with args.corpus.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid json: {exc}")
                continue
            if not any(str(row.get(k, "")).strip() for k in TEXT_KEYS):
                errors.append(f"line {line_no}: missing text field")
            rows.append(row)
    image_rows = sum(1 for row in rows if any(row.get(k) for k in IMAGE_KEYS))
    print(f"records: {len(rows)}")
    print(f"records_with_image_ref: {image_rows}")
    if not rows:
        errors.append("corpus is empty")
    if errors:
        print("valid: false")
        for error in errors[:20]:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
