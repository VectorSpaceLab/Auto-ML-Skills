#!/usr/bin/env python3
"""Validate slime coding-agent RL JSONL rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate coding-agent RL JSONL input.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--require-image-key", default="")
    args = parser.parse_args()

    rows = 0
    errors: list[str] = []
    with args.input.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            rows += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            for key in ("prompt", "label", "metadata"):
                if key not in row:
                    errors.append(f"line {line_no}: missing {key!r}")
            meta = row.get("metadata")
            if not isinstance(meta, dict):
                errors.append(f"line {line_no}: metadata must be an object")
                continue
            if not (meta.get("problem_statement") or row.get("prompt")):
                errors.append(f"line {line_no}: missing problem_statement and prompt fallback")
            if not meta.get("workdir"):
                errors.append(f"line {line_no}: metadata.workdir is required")
            if args.require_image_key and args.require_image_key not in meta:
                errors.append(f"line {line_no}: metadata missing image key {args.require_image_key!r}")
            has_grader = any(k in meta for k in ("eval_cmd", "swepro")) or (
                isinstance(meta.get("remote_env_info"), dict) and meta["remote_env_info"].get("f2p_script")
            )
            if not has_grader:
                errors.append(f"line {line_no}: no eval_cmd, swepro, or remote_env_info.f2p_script grader")

    if rows == 0:
        errors.append("input contains no JSONL rows")
    if errors:
        print("INVALID")
        for err in errors[:50]:
            print(err)
        if len(errors) > 50:
            print(f"... {len(errors) - 50} more errors")
        return 1
    print(f"OK: {rows} coding-agent rows validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
