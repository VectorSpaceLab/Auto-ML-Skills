#!/usr/bin/env python3
"""No-key smoke for Agent Inbox-style HumanInterrupt payloads."""

from __future__ import annotations

import json

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    approved: bool


def approval_node(state: State) -> dict[str, bool]:
    request = {
        "action_request": {"action": "approve", "args": {"item": "demo"}},
        "config": {
            "allow_accept": True,
            "allow_ignore": True,
            "allow_respond": True,
            "allow_edit": False,
        },
        "description": "Approve demo action.",
    }
    response = interrupt([request])[0]
    return {"approved": response.get("type") == "accept"}


def main() -> int:
    builder = StateGraph(State)
    builder.add_node("approval", approval_node)
    builder.add_edge(START, "approval")
    builder.add_edge("approval", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "human-inbox-smoke"}}

    paused = graph.invoke({"approved": False}, config)
    interrupts = graph.get_state(config).interrupts
    resumed = graph.invoke(Command(resume=[{"type": "accept"}]), config)
    result = {
        "paused_has_interrupt": "__interrupt__" in paused,
        "interrupt_count": len(interrupts),
        "resumed": resumed,
    }
    result["pass"] = result["paused_has_interrupt"] and result["interrupt_count"] == 1 and resumed["approved"] is True
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
