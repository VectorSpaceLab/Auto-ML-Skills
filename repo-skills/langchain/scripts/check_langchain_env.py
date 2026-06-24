#!/usr/bin/env python3
"""Check public LangChain package imports without requiring API keys."""

from __future__ import annotations

import argparse
import importlib
import json
from importlib import metadata


DEFAULT_MODULES = [
    "langchain",
    "langchain_core",
    "langchain_community",
    "langchain_text_splitters",
    "langsmith",
]


def check_module(name: str) -> dict[str, object]:
    result: dict[str, object] = {"module": name, "importable": False}
    try:
        module = importlib.import_module(name)
        result["importable"] = True
        result["module_file_present"] = bool(getattr(module, "__file__", None))
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    package_name = name.replace("_", "-")
    try:
        result["version"] = metadata.version(package_name)
    except metadata.PackageNotFoundError:
        if name == "langchain_core":
            lookup = "langchain-core"
        elif name == "langchain_community":
            lookup = "langchain-community"
        elif name == "langchain_text_splitters":
            lookup = "langchain-text-splitters"
        else:
            lookup = package_name
        try:
            result["version"] = metadata.version(lookup)
        except metadata.PackageNotFoundError:
            result["version"] = None
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", action="append", default=[], help="Extra module to import.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    modules = DEFAULT_MODULES + args.module
    results = [check_module(name) for name in modules]
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for row in results:
            status = "ok" if row["importable"] else "missing"
            version = row.get("version") or "unknown"
            print(f"{row['module']}: {status} version={version}")
            if "error" in row:
                print(f"  {row['error']}")
    required_ok = all(row["importable"] for row in results[:2])
    return 0 if required_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
