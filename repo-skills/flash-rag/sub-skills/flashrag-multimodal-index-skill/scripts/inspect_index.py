#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-dir", type=Path, required=True)
    args = parser.parse_args()
    if not args.index_dir.exists():
        print("valid: false")
        print("- index dir missing")
        return 1
    files = sorted([p for p in args.index_dir.rglob("*") if p.is_file()])
    for path in files[:80]:
        print(f"- {path.relative_to(args.index_dir)} ({path.stat().st_size} bytes)")
    fake = args.index_dir / "fake_mm_index.json"
    if fake.exists():
        rows = json.loads(fake.read_text(encoding="utf-8"))
        print(f"fake_index_records: {len(rows)}")
    ok = bool(files)
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
