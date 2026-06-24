#!/usr/bin/env python3
"""Check a public FlashRAG environment without using a source checkout.

Example:
  python scripts/check_flash_rag_env.py
"""
from __future__ import annotations

import importlib
import importlib.metadata as metadata
import argparse
import sys

PACKAGES = ["flashrag", "datasets", "numpy", "yaml", "torch", "transformers", "tqdm", "bm25s"]
DIST = {"yaml": "PyYAML"}
REQUIRED = {"flashrag", "datasets", "numpy", "yaml"}


def version(name: str) -> str:
    try:
        return metadata.version(DIST.get(name, name))
    except metadata.PackageNotFoundError:
        return "not installed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a public FlashRAG package environment.")
    parser.parse_args()

    print(f"python: {sys.executable}")
    errors = []
    for name in PACKAGES:
        try:
            module = importlib.import_module(name)
            where = getattr(module, "__file__", "imported")
        except Exception as exc:
            where = f"import failed: {type(exc).__name__}: {exc}"
            if name in REQUIRED:
                errors.append(f"{name} is required")
        print(f"{name}: {version(name)}; {where}")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
