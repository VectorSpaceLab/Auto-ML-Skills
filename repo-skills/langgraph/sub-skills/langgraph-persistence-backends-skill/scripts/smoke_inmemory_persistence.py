#!/usr/bin/env python3
"""No-key LangGraph InMemorySaver persistence smoke."""

from __future__ import annotations

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    count: int


def inc(state: State) -> State:
    return {"count": state.get("count", 0) + 1}


def main() -> int:
    builder = StateGraph(State)
    builder.add_node("inc", inc)
    builder.add_edge(START, "inc")
    builder.add_edge("inc", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "demo"}}
    first = graph.invoke({"count": 0}, config)
    second = graph.invoke(first, config)
    print({"valid": second["count"] == 2, "first": first, "second": second})
    return 0 if second["count"] == 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
