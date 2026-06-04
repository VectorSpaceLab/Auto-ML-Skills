#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    if not args.summary.is_file():
        print("valid: false")
        print("- summary file missing")
        return 1
    payload = json.loads(args.summary.read_text(encoding="utf-8"))
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    ok = payload.get("turns", 0) > 0 and payload.get("records") and payload["records"][-1].get("output")
    print(f"valid: {str(bool(ok)).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
