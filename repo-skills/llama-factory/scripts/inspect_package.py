#!/usr/bin/env python3
"""Read-only import/signature helper for installed packages.

Examples:
  python scripts/inspect_package.py llamafactory llamafactory.cli:main
  python scripts/inspect_package.py flashrag flashrag.config:Config
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import json
from typing import Any


def resolve(target: str) -> Any:
    module_name, _, attr = target.partition(":")
    module = importlib.import_module(module_name)
    obj: Any = module
    if attr:
        for part in attr.split("."):
            obj = getattr(obj, part)
    return obj


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package")
    parser.add_argument("targets", nargs="*")
    args = parser.parse_args()
    package = importlib.import_module(args.package)
    print(json.dumps({"package": args.package, "file": getattr(package, "__file__", None)}, indent=2))
    for target in args.targets:
        obj = resolve(target)
        try:
            signature = str(inspect.signature(obj))
        except (TypeError, ValueError):
            signature = None
        doc = inspect.getdoc(obj)
        print(json.dumps({"target": target, "signature": signature, "doc": (doc or "")[:1200]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
