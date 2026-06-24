#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()
    info_path = args.dataset_dir / "dataset_info.json"
    if not info_path.is_file():
        print(f"missing dataset_info.json: {info_path}")
        return 1
    info = json.loads(info_path.read_text(encoding="utf-8"))
    names = [item.strip() for item in args.dataset.split(",") if item.strip()]
    errors = []
    for name in names:
        meta = info.get(name)
        if meta is None:
            errors.append(f"{name}: not registered")
            continue
        if meta.get("ranking"):
            errors.append(f"{name}: ranking data is for RM/DPO, not PPO prompt data")
        print(f"{name}: {json.dumps(meta, ensure_ascii=False)}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"datasets: {len(names)}")
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
