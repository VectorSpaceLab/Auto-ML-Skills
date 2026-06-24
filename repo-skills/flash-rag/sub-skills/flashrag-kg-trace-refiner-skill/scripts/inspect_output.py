#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--save-root", type=Path, default=None)
    args = parser.parse_args()
    ok = False
    if args.summary.is_file():
        payload = json.loads(args.summary.read_text(encoding="utf-8"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        ok = payload.get("records", 0) > 0 and Path(payload.get("triple_cache", "")).exists()
    if args.save_root and args.save_root.exists():
        for path in sorted(args.save_root.rglob("*"))[:60]:
            if path.is_file():
                print(f"- {path}")
                ok = ok or path.name in {"save_triples.json", "intermediate_data.json"}
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
