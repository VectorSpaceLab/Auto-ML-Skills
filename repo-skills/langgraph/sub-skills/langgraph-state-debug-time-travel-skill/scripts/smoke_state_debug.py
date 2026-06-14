#!/usr/bin/env python3
"""No-key smoke for LangGraph state inspection and update_state."""

from __future__ import annotations

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    value: int


def inc(state: State) -> State:
    return {"value": state["value"] + 1}


def main() -> int:
    builder = StateGraph(State)
    builder.add_node("inc", inc)
    builder.add_edge(START, "inc")
    builder.add_edge("inc", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "debug-demo"}}
    out = graph.invoke({"value": 1}, config)
    state = graph.get_state(config)
    history = list(graph.get_state_history(config))
    graph.update_state(config, {"value": 10}, as_node="inc")
    repaired = graph.get_state(config)
    ok = out["value"] == 2 and state.values["value"] == 2 and repaired.values["value"] == 10 and len(history) >= 1
    print({"valid": ok, "history": len(history), "before": state.values, "after": repaired.values})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
