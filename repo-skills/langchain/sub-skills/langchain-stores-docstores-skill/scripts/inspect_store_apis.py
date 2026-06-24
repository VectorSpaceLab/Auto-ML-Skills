#!/usr/bin/env python3
"""Inspect LangChain store and docstore API imports."""

from __future__ import annotations

import importlib
import inspect
import json


TARGETS = [
    "langchain_core.stores.InMemoryStore",
    "langchain_core.stores.InMemoryByteStore",
    "langchain_core.stores.BaseStore",
    "langchain_core.stores.ByteStore",
    "langchain_classic.storage.create_kv_docstore",
    "langchain_classic.storage.create_lc_store",
]


def inspect_target(target: str) -> dict[str, object]:
    modname, attr = target.rsplit(".", 1)
    try:
        obj = getattr(importlib.import_module(modname), attr)
        return {"target": target, "ok": True, "signature": str(inspect.signature(obj))}
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        return {"target": target, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    rows = [inspect_target(target) for target in TARGETS]
    result = {"targets": rows, "pass": all(row["ok"] for row in rows)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
