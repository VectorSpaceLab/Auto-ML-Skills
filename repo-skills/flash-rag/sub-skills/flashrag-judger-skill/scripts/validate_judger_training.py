#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--training-data", type=Path, required=True)
    parser.add_argument("--kind", choices=["skr", "adaptive"], default="skr")
    args = parser.parse_args()
    rows = json.loads(args.training_data.read_text(encoding="utf-8"))
    errors: list[str] = []
    labels = []
    for idx, row in enumerate(rows if isinstance(rows, list) else []):
        if not str(row.get("question", "")).strip():
            errors.append(f"row {idx}: missing question")
        judgement = str(row.get("judgement", "")).strip()
        labels.append(judgement)
        if args.kind == "skr" and judgement not in {"ir_better", "ir_worse", "same"}:
            errors.append(f"row {idx}: invalid SKR judgement {judgement!r}")
    if not rows:
        errors.append("training data is empty")
    counts = Counter(labels)
    print(f"records: {len(rows) if isinstance(rows, list) else 0}")
    print("label_counts: " + json.dumps(counts, ensure_ascii=False))
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
