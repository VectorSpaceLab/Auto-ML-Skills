#!/usr/bin/env python3
"""Validate basic vLLM LoRA server settings."""

from __future__ import annotations

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--adapter", action="append", default=[], help="name=path_or_id")
    parser.add_argument("--max-loras", type=int, default=1)
    parser.add_argument("--max-lora-rank", type=int, default=64)
    args = parser.parse_args()
    issues = []
    names = []
    for item in args.adapter:
        if "=" not in item:
            issues.append(f"adapter must be name=path_or_id: {item}")
            continue
        name, target = item.split("=", 1)
        if not name or not target:
            issues.append(f"adapter name and target are required: {item}")
        names.append(name)
    if len(set(names)) != len(names):
        issues.append("adapter names must be unique")
    if args.max_loras < 1:
        issues.append("--max-loras must be >= 1")
    if args.max_lora_rank < 1:
        issues.append("--max-lora-rank must be >= 1")
    print(json.dumps({"valid": not issues, "issues": issues, "adapter_names": names}, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
