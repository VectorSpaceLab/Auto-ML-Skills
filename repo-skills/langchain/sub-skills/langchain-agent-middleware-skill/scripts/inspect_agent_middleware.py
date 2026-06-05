#!/usr/bin/env python3
"""Inspect importable LangChain agent middleware symbols."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-private", action="store_true")
    args = parser.parse_args()
    module = importlib.import_module("langchain.agents.middleware")
    symbols = []
    for name in dir(module):
        if name.startswith("_") and not args.include_private:
            continue
        obj = getattr(module, name)
        if inspect.isclass(obj) or inspect.isfunction(obj):
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = None
            symbols.append({"name": name, "type": "class" if inspect.isclass(obj) else "function", "signature": sig})
    print(json.dumps(symbols, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
