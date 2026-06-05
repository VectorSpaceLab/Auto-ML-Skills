#!/usr/bin/env python3
"""No-key compiled-graph smoke for ToolNode wrap_tool_call."""

from __future__ import annotations

import json
from typing import Annotated

from typing_extensions import TypedDict

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    messages: Annotated[list, add_messages]


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> int:
    seen: list[str] = []

    def wrapper(request, execute):  # noqa: ANN001, ANN202 - version-sensitive request object
        seen.append(type(request).__name__)
        return execute(request)

    tool_node = ToolNode([add], wrap_tool_call=wrapper)
    builder = StateGraph(State)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)
    graph = builder.compile()

    ai_message = AIMessage(
        content="",
        tool_calls=[{"name": "add", "args": {"a": 2, "b": 3}, "id": "call-1"}],
    )
    out = graph.invoke({"messages": [ai_message]})
    last = out["messages"][-1]
    result = {
        "wrapper_seen": seen,
        "last_message_type": type(last).__name__,
        "last_content": getattr(last, "content", None),
    }
    result["pass"] = seen and result["last_message_type"] == "ToolMessage" and result["last_content"] == "5"
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
