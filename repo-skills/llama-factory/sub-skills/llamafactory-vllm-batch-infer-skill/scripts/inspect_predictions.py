#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    args = parser.parse_args()
    if not args.predictions.exists():
        print("valid: false")
        print("- predictions file missing")
        return 1
    rows = [json.loads(line) for line in args.predictions.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"rows: {len(rows)}")
    if rows:
        print("first_keys: " + ",".join(sorted(rows[0].keys())))
        for key in ["prompt", "predict", "label"]:
            print(f"first_has_{key}: {str(key in rows[0]).lower()}")
    ok = bool(rows) and "predict" in rows[0]
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
