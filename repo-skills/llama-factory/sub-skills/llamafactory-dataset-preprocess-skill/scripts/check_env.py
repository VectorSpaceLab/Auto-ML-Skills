#!/usr/bin/env python3
"""Check a public package environment for LLaMA-Factory llamafactory-dataset-preprocess-skill.

This script is intentionally read-only. It checks installed packages and an
optional package root added to PYTHONPATH; it does not require a source checkout.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import sys
from pathlib import Path

REQUIRED = ['llamafactory', 'torch', 'transformers', 'datasets', 'yaml']
OPTIONAL = ['accelerate', 'peft', 'trl']
DIST = {'yaml': 'PyYAML', 'PIL': 'Pillow', 'sse_starlette': 'sse-starlette', 'rouge_chinese': 'rouge-chinese', 'llamafactory': 'llamafactory'}


def dist_name(module_name: str) -> str:
    return DIST.get(module_name, module_name)


def version(module_name: str) -> str:
    try:
        return metadata.version(dist_name(module_name))
    except metadata.PackageNotFoundError:
        return "not installed"


def import_detail(module_name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(module_name)
        return True, getattr(module, "__file__", "imported")
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH for inspection.")
    args = parser.parse_args()
    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
        print(f"package_root: {args.package_root.resolve()}")
    print(f"python: {sys.executable}")

    errors: list[str] = []
    for name in REQUIRED:
        ok, detail = import_detail(name)
        print(f"{name}: {version(name)}; {detail}")
        if not ok:
            errors.append(f"required import failed: {name}")
    for name in OPTIONAL:
        if name in REQUIRED:
            continue
        ok, detail = import_detail(name)
        print(f"{name}: {version(name)}; {detail}")
        if not ok:
            print(f"warning: optional import failed: {name}")

    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
