#!/usr/bin/env python3
"""Validate SGLang LoRA lifecycle payloads."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate load/unload LoRA adapter payloads.")
    parser.add_argument("json_file", nargs="?")
    parser.add_argument("--action", choices=["load", "unload"], default="load")
    args = parser.parse_args()
    if not args.json_file:
        print("Provide a JSON payload file; --help is lightweight.")
        return 0
    data = json.load(open(args.json_file, encoding="utf-8"))
    issues = []
    if args.action == "load":
        if not any(k in data for k in ["lora_name", "name", "adapter_name"]):
            issues.append("load payload should include lora_name/name/adapter_name")
        if not any(k in data for k in ["lora_path", "path", "adapter_path"]):
            issues.append("load payload should include lora_path/path/adapter_path")
    else:
        if not any(k in data for k in ["lora_name", "name", "adapter_name"]):
            issues.append("unload payload should include lora_name/name/adapter_name")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
