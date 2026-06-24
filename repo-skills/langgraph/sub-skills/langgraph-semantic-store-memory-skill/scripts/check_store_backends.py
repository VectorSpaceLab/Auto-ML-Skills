#!/usr/bin/env python3
"""Import-check LangGraph store backend packages without opening databases."""

from __future__ import annotations

import importlib
import json


TARGETS = [
    "langgraph.store.memory.InMemoryStore",
    "langgraph.checkpoint.sqlite",
    "langgraph.checkpoint.postgres",
]


def check(target: str) -> dict[str, object]:
    try:
        importlib.import_module(target)
        return {"target": target, "ok": True}
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        return {"target": target, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    rows = [check(target) for target in TARGETS]
    result = {"targets": rows, "pass": rows[0]["ok"]}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
