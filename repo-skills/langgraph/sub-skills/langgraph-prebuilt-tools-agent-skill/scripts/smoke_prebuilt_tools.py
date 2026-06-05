#!/usr/bin/env python3
"""No-key smoke test for ToolNode and tools_condition."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> int:
    class State(TypedDict):
        messages: list

    builder = StateGraph(State)
    builder.add_node("tools", ToolNode([add]))
    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)
    graph = builder.compile()

    ai = AIMessage(
        content="",
        tool_calls=[{"name": "add", "args": {"a": 2, "b": 5}, "id": "call-1"}],
    )
    assert tools_condition({"messages": [ai]}) == "tools"
    assert tools_condition({"messages": [HumanMessage(content="done")]}) == "__end__"
    out = graph.invoke({"messages": [ai]})
    messages = out["messages"]
    assert messages and "7" in messages[0].content, out
    print({"valid": True, "tool_messages": len(messages), "content": messages[0].content})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
