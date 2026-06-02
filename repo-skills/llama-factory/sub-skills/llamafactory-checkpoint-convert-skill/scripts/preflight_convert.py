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
    task = payload["task"]
    if task == "hf2dcp":
        hf = Path(str(payload.get("hf_path")))
        if not (hf / "config.json").is_file():
            errors.append(f"hf_path must contain config.json: {hf}")
        if not payload.get("dcp_path"):
            errors.append("dcp_path is required")
    elif task == "dcp2hf":
        dcp = Path(str(payload.get("dcp_path")))
        cfg = Path(str(payload.get("config_path")))
        if not dcp.exists():
            errors.append(f"dcp_path does not exist: {dcp}")
        if not (cfg / "config.json").is_file():
            errors.append(f"config_path must contain config.json: {cfg}")
        if not payload.get("hf_path"):
            errors.append("hf_path is required")
    elif len(payload.get("command", [])) <= 2:
        print("warning: pass-through conversion command has no extra args; it will likely show usage or fail")
    print(f"task: {task}")
    print(f"script: {script}")
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
