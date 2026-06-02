#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def read_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def is_url(text: str) -> bool:
    return bool(re.match(r"https?://", text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    errors = []
    if cfg.get("stage") != "ppo":
        errors.append("stage must be ppo")
    reward_model = cfg.get("reward_model")
    reward_type = cfg.get("reward_model_type", "lora")
    method = cfg.get("finetuning_type")
    if not reward_model or reward_model in {"null", "None"}:
        errors.append("reward_model is required")
    elif reward_type == "api" and not is_url(reward_model):
        errors.append("reward_model_type api requires reward_model to be an http(s) URL")
    elif reward_type != "api" and not Path(reward_model).exists():
        print(f"warning: reward_model path does not exist locally yet: {reward_model}")
    if reward_type == "lora" and method != "lora":
        errors.append("reward_model_type lora requires finetuning_type lora")
    print(f"stage: {cfg.get('stage')}")
    print(f"finetuning_type: {method}")
    print(f"reward_model_type: {reward_type}")
    print(f"reward_model: {reward_model}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
