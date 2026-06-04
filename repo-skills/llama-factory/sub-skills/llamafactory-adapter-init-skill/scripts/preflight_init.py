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
    model_raw = str(payload["model_name_or_path"])
    model = Path(model_raw)
    output_dir = Path(payload["output_dir"])
    warnings: list[str] = []
    cmd = payload.get("command") or []
    if not script.is_file():
        errors.append(f"init script does not exist: {script}")
    remote_like = "/" in model_raw and not model_raw.startswith((".", "/"))
    if not model.exists() and not remote_like:
        errors.append(f"model path does not exist: {model}")
    elif not model.exists() and remote_like:
        warnings.append(f"model looks like a remote model id and will be resolved by the model loader: {model_raw}")
    if "--lora-rank" in cmd:
        rank = int(cmd[cmd.index("--lora-rank") + 1])
        if rank <= 0:
            errors.append("lora rank must be positive")
    if payload["kind"] == "loftq" and "--loftq-bits" in cmd:
        bits = int(cmd[cmd.index("--loftq-bits") + 1])
        if bits not in {2, 3, 4, 8}:
            errors.append("loftq bits should normally be one of 2, 3, 4, 8")
    print(f"kind: {payload['kind']}")
    print(f"script: {script}")
    print(f"model: {model}")
    print(f"output_dir: {output_dir}")
    print("handoff: " + json.dumps(payload["handoff"], ensure_ascii=False))
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"- {warning}")
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
