#!/usr/bin/env python3
"""Inspect SQL and graph toolkit imports without opening external connections."""

from __future__ import annotations

import importlib
import inspect
import json


TARGETS = [
    "langchain_classic.chains.create_sql_query_chain",
    "langchain_community.utilities.SQLDatabase",
    "langchain_community.agent_toolkits.sql.toolkit.SQLDatabaseToolkit",
    "langchain_community.agent_toolkits.sql.base.create_sql_agent",
    "langchain_community.tools.InfoSQLDatabaseTool",
    "langchain_community.tools.ListSQLDatabaseTool",
    "langchain_community.chains.graph_qa.cypher.GraphCypherQAChain",
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
    required = [row for row in rows if "GraphCypherQAChain" not in row["target"]]
    result = {"targets": rows, "pass": all(row["ok"] for row in required)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
