#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.command.read_text(encoding="utf-8"))
    errors: list[str] = []
    script = Path(payload["script"])
    if not script.is_file():
        errors.append(f"script does not exist: {script}")
    if payload["task"] in {"length-cdf", "flops", "mfu", "bench-qwen"}:
        model = Path(str(payload.get("model")))
        if not model.exists():
            errors.append(f"model path does not exist: {model}")
    if payload["task"] == "length-cdf":
        dataset_dir = Path(str(payload.get("dataset_dir")))
        if not dataset_dir.exists():
            errors.append(f"dataset_dir does not exist: {dataset_dir}")
    print(f"task: {payload['task']}")
    print("command: " + " ".join(payload["command"]))
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
