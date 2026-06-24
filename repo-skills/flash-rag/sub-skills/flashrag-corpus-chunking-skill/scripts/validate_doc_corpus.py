#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import load_jsonl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=20)
    args = parser.parse_args()
    rows = load_jsonl(args.input)
    errors: list[str] = []
    for idx, row in enumerate(rows[: args.max_rows]):
        if "id" not in row:
            errors.append(f"row {idx} missing id")
        if not isinstance(row.get("contents"), str) or not row.get("contents", "").strip():
            errors.append(f"row {idx} missing non-empty contents")
    print(f"rows: {len(rows)}")
    if rows:
        print("first_preview: " + rows[0].get("contents", "")[:160].replace("\n", " "))
    if not rows:
        errors.append("empty corpus")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
