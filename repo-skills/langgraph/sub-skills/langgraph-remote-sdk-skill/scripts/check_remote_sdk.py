#!/usr/bin/env python3
"""No-network import inspection for the LangGraph Python SDK."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    try:
        sdk = importlib.import_module("langgraph_sdk")
    except Exception as exc:
        print(json.dumps({"importable": False, "error": f"{type(exc).__name__}: {exc}"}, indent=2))
        return 1
    symbols = []
    for name in dir(sdk):
        if name.startswith("_"):
            continue
        obj = getattr(sdk, name)
        if inspect.isfunction(obj) or inspect.isclass(obj):
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = None
            symbols.append({"name": name, "type": "class" if inspect.isclass(obj) else "function", "signature": sig})
    print(json.dumps({"importable": True, "symbols": symbols}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
