#!/usr/bin/env python3
"""Inspect LangGraph functional API symbols."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-private", action="store_true")
    args = parser.parse_args()
    module = importlib.import_module("langgraph.func")
    out = []
    for name in dir(module):
        if name.startswith("_") and not args.include_private:
            continue
        obj = getattr(module, name)
        if inspect.isfunction(obj) or inspect.isclass(obj):
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = None
            out.append({"name": name, "type": "class" if inspect.isclass(obj) else "function", "signature": sig})
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
