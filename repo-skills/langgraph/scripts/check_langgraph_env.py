#!/usr/bin/env python3
"""Safe public-package import check for LangGraph."""

from __future__ import annotations

import importlib
import importlib.metadata as md
import json


PACKAGES = [
    ("langgraph", "langgraph"),
    ("langgraph-checkpoint", "langgraph.checkpoint"),
    ("langgraph-cli", "langgraph_cli"),
    ("langgraph-checkpoint-sqlite", "langgraph.checkpoint.sqlite"),
    ("langgraph-checkpoint-postgres", "langgraph.checkpoint.postgres"),
]


def main() -> int:
    results = []
    for dist, module in PACKAGES:
        item = {"distribution": dist, "module": module}
        try:
            mod = importlib.import_module(module)
            item["import"] = "ok"
            item["module_file"] = bool(getattr(mod, "__file__", None))
        except Exception as exc:  # noqa: BLE001
            item["import"] = "missing"
            item["error"] = f"{type(exc).__name__}: {exc}"
        try:
            item["version"] = md.version(dist)
        except md.PackageNotFoundError:
            item["version"] = None
        results.append(item)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if results[0]["import"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
