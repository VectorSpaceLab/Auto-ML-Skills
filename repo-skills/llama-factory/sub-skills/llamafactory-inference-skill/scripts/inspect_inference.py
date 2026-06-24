#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect chat or batch prediction output.")
    parser.add_argument("--output", type=Path, required=True, help="JSONL file or prediction output directory.")
    args = parser.parse_args()

    target = args.output
    if target.is_dir():
        pred = target / "generated_predictions.jsonl"
    else:
        pred = target
    print(f"prediction_file: {pred.resolve()}")
    if not pred.is_file():
        print("valid: false")
        print("- prediction file does not exist")
        return 1
    rows = _load_jsonl(pred)
    print(f"rows: {len(rows)}")
    if rows:
        print("first_row: " + json.dumps(rows[0], ensure_ascii=False))
    errors: list[str] = []
    if not rows:
        errors.append("prediction file is empty")
    for idx, row in enumerate(rows[:10]):
        text = row.get("response", row.get("predict", ""))
        if not isinstance(text, str) or not text.strip():
            errors.append(f"row {idx}: generated text is empty")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
