#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import load_jsonl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=20)
    args = parser.parse_args()
    rows = load_jsonl(args.corpus)
    errors = []
    for i, row in enumerate(rows[: args.max_rows]):
        if "id" not in row:
            errors.append(f"row {i} missing id")
        if not row.get("contents"):
            errors.append(f"row {i} missing contents")
    print(f"records: {len(rows)}")
    if rows:
        print("first_preview: " + str(rows[0].get("contents", ""))[:160].replace("\n", " "))
    if not rows:
        errors.append("empty corpus")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
