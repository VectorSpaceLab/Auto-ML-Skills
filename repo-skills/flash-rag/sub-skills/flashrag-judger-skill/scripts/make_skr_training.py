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
        {"question": "Who wrote Hamlet?", "judgement": "ir_better"},
        {"question": "What is 2+2?", "judgement": "ir_worse"},
        {"question": "Where is the Eiffel Tower?", "judgement": "ir_better"},
        {"question": "Say hello.", "judgement": "same"},
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
