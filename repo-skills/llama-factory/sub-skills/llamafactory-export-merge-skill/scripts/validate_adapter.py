#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PEFT adapter directory before LLaMA-Factory export.")
    parser.add_argument("--adapter", type=Path, required=True)
    args = parser.parse_args()

    adapter = args.adapter
    errors: list[str] = []
    if not adapter.is_dir():
        errors.append("adapter directory does not exist")
    cfg_path = adapter / "adapter_config.json"
    if not cfg_path.is_file():
        errors.append("adapter_config.json is missing")
    else:
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            print(f"peft_type: {cfg.get('peft_type')}")
            print(f"base_model_name_or_path: {cfg.get('base_model_name_or_path')}")
            if cfg.get("peft_type") != "LORA":
                errors.append("this skill expects a LoRA adapter with peft_type=LORA")
        except Exception as exc:
            errors.append(f"adapter_config.json is not valid JSON: {exc}")
    if not ((adapter / "adapter_model.safetensors").is_file() or (adapter / "adapter_model.bin").is_file()):
        errors.append("adapter_model.safetensors or adapter_model.bin is missing")

    print(f"adapter: {adapter.resolve()}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
