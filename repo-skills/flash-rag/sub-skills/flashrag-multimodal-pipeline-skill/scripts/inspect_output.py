#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--save-root", type=Path, default=None)
    args = parser.parse_args()
    ok = False
    if args.summary and args.summary.is_file():
        payload = json.loads(args.summary.read_text(encoding="utf-8"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        ok = payload.get("records", 0) > 0 and bool(payload.get("first_pred"))
    if args.save_root and args.save_root.exists():
        print(f"save_root: {args.save_root.resolve()}")
        for path in sorted(args.save_root.rglob("*"))[:40]:
            if path.is_file():
                print(f"- {path}")
                ok = ok or path.name in {"intermediate_data.json", "metric_score.txt"}
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
