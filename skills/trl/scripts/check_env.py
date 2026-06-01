#!/usr/bin/env python
"""Check a Python environment for TRL core and optional dependencies.

This script is safe by default: it imports packages and prints versions only.

Example:
    python scripts/check_env.py
    python scripts/check_env.py --optional
"""

from __future__ import annotations

import argparse
import importlib
import platform
import sys
from importlib.metadata import PackageNotFoundError, version


CORE_PACKAGES = ["trl", "transformers", "accelerate", "datasets", "torch"]
OPTIONAL_PACKAGES = [
    "peft",
    "bitsandbytes",
    "vllm",
    "liger_kernel",
    "kernels",
    "deepspeed",
    "PIL",
    "torchvision",
    "math_verify",
    "openreward",
]


def package_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not installed"


def import_status(module_name: str) -> str:
    try:
        importlib.import_module(module_name)
    except Exception as exc:
        return f"import failed: {exc.__class__.__name__}: {exc}"
    return "import ok"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--optional", action="store_true", help="Also check optional TRL backend packages.")
    args = parser.parse_args()

    print(f"python: {sys.version.split()[0]} ({platform.platform()})")
    for package in CORE_PACKAGES:
        module = "PIL" if package == "pillow" else package
        print(f"{package}: {package_version(package)}; {import_status(module)}")

    if args.optional:
        for module in OPTIONAL_PACKAGES:
            distribution = "Pillow" if module == "PIL" else module.replace("_", "-")
            print(f"{module}: {package_version(distribution)}; {import_status(module)}")

    try:
        import trl

        names = [
            "SFTTrainer",
            "DPOTrainer",
            "GRPOTrainer",
            "RLOOTrainer",
            "RewardTrainer",
            "SFTConfig",
            "DPOConfig",
            "GRPOConfig",
            "RLOOConfig",
            "RewardConfig",
        ]
        missing = [name for name in names if not hasattr(trl, name)]
        print(f"trl version: {getattr(trl, '__version__', 'unknown')}")
        print("trl stable imports:", "ok" if not missing else f"missing {missing}")
    except Exception as exc:
        print(f"trl public API check failed: {exc.__class__.__name__}: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
