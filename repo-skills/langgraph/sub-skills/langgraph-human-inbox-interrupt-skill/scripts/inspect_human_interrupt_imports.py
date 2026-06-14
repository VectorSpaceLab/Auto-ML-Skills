#!/usr/bin/env python3
"""Inspect LangGraph human interrupt schema imports."""

from __future__ import annotations

import importlib
import inspect
import json


TARGETS = [
    "langgraph.types.interrupt",
    "langgraph.types.Command",
    "langgraph.prebuilt.interrupt.HumanInterrupt",
    "langgraph.prebuilt.interrupt.HumanResponse",
]


def inspect_target(target: str) -> dict[str, object]:
    modname, attr = target.rsplit(".", 1)
    try:
        obj = getattr(importlib.import_module(modname), attr)
        sig = str(inspect.signature(obj)) if callable(obj) else ""
        return {"target": target, "ok": True, "signature": sig}
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        return {"target": target, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    rows = [inspect_target(target) for target in TARGETS]
    result = {"targets": rows, "pass": rows[0]["ok"] and rows[1]["ok"]}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
