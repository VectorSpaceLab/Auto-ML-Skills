#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def read_simple_yaml(path: Path) -> dict[str, str]:
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    errors = []
    stage = cfg.get("stage")
    ftype = cfg.get("finetuning_type")
    if ftype not in {"lora", "oft"}:
        errors.append("finetuning_type must be lora or oft")
    if cfg.get("pissa_init") == "true" and stage in {"ppo", "kto"}:
        errors.append("PiSSA init is not supported for PPO/KTO")
    if ftype == "oft" and not cfg.get("oft_target"):
        errors.append("oft_target is required for OFT")
    if ftype == "lora" and not cfg.get("lora_target"):
        errors.append("lora_target is required for LoRA variants")
    print(f"stage: {stage}")
    print(f"finetuning_type: {ftype}")
    for key in ["loraplus_lr_ratio", "use_rslora", "use_dora", "pissa_init", "pissa_convert", "oft_block_size"]:
        if key in cfg:
            print(f"{key}: {cfg[key]}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
