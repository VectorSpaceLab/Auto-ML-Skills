#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [
        {
            "id": "trace-1",
            "question": "Who wrote Hamlet?",
            "golden_answers": ["William Shakespeare"],
            "retrieval_result": [
                {"id": "doc-1", "contents": "Hamlet\nHamlet is a tragedy written by William Shakespeare."},
                {"id": "doc-2", "contents": "Shakespeare\nWilliam Shakespeare was an English playwright."},
            ],
        }
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
