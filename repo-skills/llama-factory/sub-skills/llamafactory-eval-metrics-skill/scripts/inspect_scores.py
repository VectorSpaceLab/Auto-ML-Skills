#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--score-file", type=Path, required=True)
    args = parser.parse_args()
    print(f"score_file: {args.score_file.resolve()}")
    if not args.score_file.is_file():
        print("valid: false")
        print("- score file missing")
        return 1
    data = json.loads(args.score_file.read_text(encoding="utf-8"))
    print(json.dumps(data, ensure_ascii=False, indent=2))
    ok = isinstance(data, dict) and bool(data)
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
