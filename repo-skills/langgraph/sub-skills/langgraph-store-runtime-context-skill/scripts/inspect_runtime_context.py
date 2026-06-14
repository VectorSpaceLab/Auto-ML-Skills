#!/usr/bin/env python3
"""Inspect LangGraph runtime/context/store public symbols."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json

OBJECTS = ["langgraph.store.memory.InMemoryStore", "langgraph.runtime.Runtime"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    out = []
    for path in OBJECTS:
        mod, name = path.rsplit(".", 1)
        try:
            obj = getattr(importlib.import_module(mod), name)
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = None
            out.append({"path": path, "importable": True, "signature": sig})
        except Exception as exc:
            out.append({"path": path, "importable": False, "error": f"{type(exc).__name__}: {exc}"})
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
