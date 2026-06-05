#!/usr/bin/env python3
"""Inspect LangGraph node policy API signatures."""

from __future__ import annotations

import importlib
import inspect
import json


TARGETS = [
    "langgraph.graph.StateGraph.add_node",
    "langgraph.graph.StateGraph.compile",
    "langgraph.types.RetryPolicy",
    "langgraph.types.CachePolicy",
    "langgraph.cache.memory.InMemoryCache",
]


def inspect_target(target: str) -> dict[str, object]:
    parts = target.split(".")
    modname = ".".join(parts[:-1])
    attr = parts[-1]
    try:
        obj = getattr(importlib.import_module(modname), attr)
    except Exception:
        modname = ".".join(parts[:-2])
        cls = getattr(importlib.import_module(modname), parts[-2])
        obj = getattr(cls, attr)
    return {"target": target, "ok": True, "signature": str(inspect.signature(obj))}


def main() -> int:
    rows = []
    for target in TARGETS:
        try:
            rows.append(inspect_target(target))
        except Exception as exc:  # noqa: BLE001 - diagnostic script
            rows.append({"target": target, "ok": False, "error": f"{type(exc).__name__}: {exc}"})
    result = {"targets": rows, "pass": all(row["ok"] for row in rows)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
