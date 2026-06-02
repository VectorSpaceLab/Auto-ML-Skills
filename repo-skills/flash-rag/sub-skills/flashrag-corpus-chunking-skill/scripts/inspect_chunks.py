#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import load_jsonl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.output.exists():
        print("valid: false")
        print("- output missing")
        return 1
    rows = load_jsonl(args.output)
    print(f"chunks: {len(rows)}")
    errors: list[str] = []
    if rows:
        first = rows[0]
        print("first_keys: " + ",".join(sorted(first.keys())))
        print("first_preview: " + first.get("contents", "")[:180].replace("\n", " "))
        for key in ["id", "doc_id", "title", "contents"]:
            if key not in first:
                errors.append(f"first chunk missing {key}")
    else:
        errors.append("no chunks")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
