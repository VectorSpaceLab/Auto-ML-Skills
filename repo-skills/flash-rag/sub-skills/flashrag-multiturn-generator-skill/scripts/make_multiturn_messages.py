#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--system", default="You are a helpful assistant. Answer concisely.")
    parser.add_argument("--turn1", default="Who wrote Hamlet?")
    parser.add_argument("--turn2", default="Give only the surname.")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": args.system},
        {"role": "user", "content": args.turn1},
        {"role": "user", "content": args.turn2},
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(messages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
