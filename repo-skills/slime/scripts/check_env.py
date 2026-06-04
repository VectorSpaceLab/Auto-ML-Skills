#!/usr/bin/env python3
"""Check whether a Python environment can import slime and, optionally, its Megatron training stack.

Example:
  python check_env.py
  python check_env.py --strict-train --megatron-path /path/to/Megatron-LM

This script is read-only. It does not start Ray, allocate GPUs, download models, or mutate files.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import importlib.util
import json
import sys
from pathlib import Path


def module_ok(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    result = {"module": name, "found": spec is not None}
    if spec is not None:
        result["origin_kind"] = "namespace" if spec.origin is None else "module"
    return result


def import_ok(name: str) -> dict:
    try:
        module = importlib.import_module(name)
        return {"module": name, "ok": True, "package": getattr(module, "__package__", None)}
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        return {"module": name, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a slime Python environment.")
    parser.add_argument("--strict-train", action="store_true", help="Also verify Megatron-backed training imports.")
    parser.add_argument(
        "--megatron-path",
        type=Path,
        default=None,
        help="Optional full Megatron-LM checkout to prepend to sys.path for strict training checks.",
    )
    args = parser.parse_args()

    if args.megatron_path is not None:
        sys.path.insert(0, str(args.megatron_path))

    report: dict[str, object] = {
        "python": sys.version.split()[0],
        "distribution": None,
        "modules": [],
        "imports": [],
        "strict_train": args.strict_train,
    }

    try:
        report["distribution"] = {
            "name": "slime",
            "version": metadata.version("slime"),
            "requirements": metadata.requires("slime") or [],
            "console_scripts": [
                ep.name
                for ep in metadata.entry_points().select(group="console_scripts")
                if ep.value.startswith("slime")
            ],
        }
    except Exception as exc:  # noqa: BLE001
        report["distribution"] = {"name": "slime", "error": f"{type(exc).__name__}: {exc}"}

    modules = [
        "slime",
        "slime_plugins",
        "slime.rollout.base_types",
        "slime.utils.types",
        "slime.rollout.sglang_rollout",
        "slime.rollout.sft_rollout",
        "slime.backends.sglang_utils.arguments",
    ]
    if args.strict_train:
        modules.extend(
            [
                "megatron.training.arguments",
                "slime.backends.megatron_utils.arguments",
                "slime.ray.placement_group",
            ]
        )

    report["modules"] = [module_ok(name) for name in modules]
    report["imports"] = [import_ok(name) for name in modules]

    print(json.dumps(report, indent=2, sort_keys=True))

    failures = [item for item in report["imports"] if not item.get("ok")]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
