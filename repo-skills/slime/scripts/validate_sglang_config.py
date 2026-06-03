#!/usr/bin/env python3
"""Lightweight validator for slime `--sglang-config` YAML files.

This does not import SGLang or start servers. It catches structural mistakes
before a Ray job consumes GPU resources.
"""

from __future__ import annotations

import argparse
from pathlib import Path


VALID_WORKER_TYPES = {"regular", "prefill", "decode", "placeholder"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a slime SGLang config YAML.")
    parser.add_argument("config", type=Path)
    parser.add_argument("--expected-rollout-gpus", type=int, default=None)
    args = parser.parse_args()

    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "PyYAML is required to validate SGLang config files. Install it with `pip install pyyaml` "
            "or run this script in the slime runtime environment."
        ) from exc

    data = yaml.safe_load(args.config.read_text()) or {}
    models = data.get("sglang", data if isinstance(data, list) else None)
    if not isinstance(models, list) or not models:
        raise SystemExit("Config must define a non-empty `sglang:` list.")

    total_gpus = 0
    names: set[str] = set()
    for i, model in enumerate(models):
        if not isinstance(model, dict):
            raise SystemExit(f"Model entry {i} must be a mapping.")
        name = model.get("name")
        if not name:
            raise SystemExit(f"Model entry {i} is missing `name`.")
        if name in names:
            raise SystemExit(f"Duplicate model name: {name}")
        names.add(name)

        groups = model.get("server_groups")
        if not isinstance(groups, list) or not groups:
            raise SystemExit(f"Model {name} must define non-empty `server_groups`.")
        for j, group in enumerate(groups):
            worker_type = group.get("worker_type")
            if worker_type not in VALID_WORKER_TYPES:
                raise SystemExit(f"Model {name} group {j} has invalid worker_type {worker_type!r}.")
            num_gpus = group.get("num_gpus")
            if not isinstance(num_gpus, int) or num_gpus <= 0:
                raise SystemExit(f"Model {name} group {j} must set positive integer num_gpus.")
            total_gpus += num_gpus
            tp = group.get("num_gpus_per_engine", model.get("num_gpus_per_engine"))
            if tp is not None and (not isinstance(tp, int) or tp <= 0 or num_gpus % tp != 0):
                raise SystemExit(f"Model {name} group {j} has invalid num_gpus_per_engine={tp}.")

    if args.expected_rollout_gpus is not None and total_gpus != args.expected_rollout_gpus:
        raise SystemExit(
            f"Config describes {total_gpus} rollout GPUs, expected {args.expected_rollout_gpus}."
        )

    print(f"OK: {len(models)} model(s), {total_gpus} rollout GPU(s) described.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
