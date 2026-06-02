#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    if args.summary:
        if not args.summary.is_file():
            print("valid: false")
            print("- summary is missing")
            return 1
        payload = json.loads(args.summary.read_text(encoding="utf-8"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        ok = payload.get("records", 0) > 0 and isinstance(payload.get("metrics"), dict)
        print(f"valid: {str(ok).lower()}")
        return 0 if ok else 1

    if args.output_dir is None:
        print("valid: false")
        print("- provide --summary or --output-dir")
        return 1
    path = args.output_dir
    print(f"output_dir: {path.resolve()}")
    if not path.is_dir():
        print("valid: false")
        return 1
    names = {p.name for p in path.iterdir()}
    for name in sorted(names):
        print(f"- {name}")
    ok = {"metric_score.txt", "intermediate_data.json", "config.yaml"}.issubset(names)
    score = path / "metric_score.txt"
    if score.exists():
        print(score.read_text(encoding="utf-8").strip())
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
