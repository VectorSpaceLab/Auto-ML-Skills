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


def truthy(value: str | None) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--world-size", type=int, default=1)
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    errors = []
    warnings = []
    grad_accum = int(cfg.get("gradient_accumulation_steps", "1"))
    if truthy(cfg.get("galore_layerwise")):
        if grad_accum != 1:
            errors.append("layer-wise GaLore requires gradient_accumulation_steps=1")
        if args.world_size > 1:
            errors.append("distributed training does not support layer-wise GaLore")
    if truthy(cfg.get("apollo_layerwise")):
        if grad_accum != 1:
            errors.append("layer-wise APOLLO requires gradient_accumulation_steps=1")
        if args.world_size > 1:
            errors.append("distributed training does not support layer-wise APOLLO")
    if truthy(cfg.get("use_badam")) and args.world_size > 1 and cfg.get("badam_mode") == "layer" and not cfg.get("deepspeed"):
        warnings.append("layer-wise BAdam in distributed settings usually needs DeepSpeed ZeRO-3")
    if truthy(cfg.get("fp8")):
        warnings.append("FP8 requires supported hardware and backend; verify torch/accelerate/backend before launch")
    for key in sorted(k for k in cfg if k.startswith("use_") or k in {"fp8", "enable_torch_profiler", "galore_layerwise", "apollo_layerwise"}):
        print(f"{key}: {cfg[key]}")
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
