#!/usr/bin/env python3
"""Import-check LangGraph checkpoint persistence backends without DB connections."""

from __future__ import annotations

import argparse
import importlib
import json

OBJECTS = [
    "langgraph.checkpoint.memory.InMemorySaver",
    "langgraph.checkpoint.sqlite.SqliteSaver",
    "langgraph.checkpoint.sqlite.aio.AsyncSqliteSaver",
    "langgraph.checkpoint.postgres.PostgresSaver",
    "langgraph.checkpoint.postgres.aio.AsyncPostgresSaver",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    out = []
    for path in OBJECTS:
        mod, name = path.rsplit(".", 1)
        try:
            obj = getattr(importlib.import_module(mod), name)
            out.append({"path": path, "importable": True, "type": type(obj).__name__})
        except Exception as exc:
            out.append({"path": path, "importable": False, "error": f"{type(exc).__name__}: {exc}"})
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
