#!/usr/bin/env python3
"""No-key smoke test for checkpointed interrupt/resume."""

from __future__ import annotations

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    question: str
    answer: str | None
    approved: bool | None


def ask(state: State) -> dict:
    approved = interrupt({"question": state["question"], "kind": "approval"})
    return {"approved": bool(approved), "answer": "approved" if approved else "rejected"}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("ask", ask)
    builder.add_edge(START, "ask")
    builder.add_edge("ask", END)
    return builder.compile(checkpointer=InMemorySaver())


def main() -> int:
    graph = build_graph()
    config = {"configurable": {"thread_id": "smoke-thread"}}
    first = graph.invoke({"question": "Ship?", "answer": None, "approved": None}, config)
    interrupts = first.get("__interrupt__")
    assert interrupts, first
    second = graph.invoke(Command(resume=True), config)
    assert second["approved"] is True and second["answer"] == "approved", second
    state = graph.get_state(config)
    history = list(graph.get_state_history(config))
    assert state.values["answer"] == "approved"
    assert history, "expected checkpoint history"
    print({"valid": True, "interrupts": len(interrupts), "history": len(history), "final": second})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
