#!/usr/bin/env python3
"""Read-only API signature helper for public LangGraph installs."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json


OBJECTS = [
    "langgraph.graph.StateGraph",
    "langgraph.graph.MessageGraph",
    "langgraph.graph.MessagesState",
    "langgraph.graph.add_messages",
    "langgraph.types.Command",
    "langgraph.types.Send",
    "langgraph.types.interrupt",
    "langgraph.prebuilt.create_react_agent",
    "langgraph.prebuilt.ToolNode",
    "langgraph.prebuilt.tools_condition",
    "langgraph.checkpoint.memory.InMemorySaver",
]


def inspect_object(path: str) -> dict[str, str]:
    module_name, name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    obj = getattr(module, name)
    try:
        signature = str(inspect.signature(obj))
    except Exception as exc:  # noqa: BLE001
        signature = f"<unavailable: {type(exc).__name__}: {exc}>"
    return {
        "path": path,
        "type": type(obj).__name__,
        "signature": signature,
        "doc_first_line": (inspect.getdoc(obj) or "").splitlines()[0:1][0]
        if inspect.getdoc(obj)
        else "",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true", help="print compact JSON")
    args = parser.parse_args()
    data = [inspect_object(path) for path in OBJECTS]
    if args.summary:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        for item in data:
            print(f"{item['path']}: {item['signature']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
