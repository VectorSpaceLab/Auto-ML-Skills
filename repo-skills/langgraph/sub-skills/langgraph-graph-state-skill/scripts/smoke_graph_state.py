#!/usr/bin/env python3
"""No-key smoke test for LangGraph graph/state primitives."""

from __future__ import annotations

import operator
from typing import Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Send


class State(TypedDict):
    items: list[str]
    done: Annotated[list[str], operator.add]
    route: str


class WorkerState(TypedDict):
    item: str


def plan(state: State):
    return [Send("worker", {"item": item}) for item in state["items"]]


def worker(state: WorkerState) -> dict:
    return {"done": [state["item"].upper()]}


def decide(state: State) -> Command[Literal["finish"]]:
    return Command(update={"route": "finish"}, goto="finish")


def finish(state: State) -> dict:
    return {"done": ["count:" + str(len(state["done"]))]}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("worker", worker)
    builder.add_node("decide", decide)
    builder.add_node("finish", finish)
    builder.add_conditional_edges(START, plan)
    builder.add_edge("worker", "decide")
    builder.add_edge("finish", END)
    return builder.compile()


def main() -> int:
    graph = build_graph()
    out = graph.invoke({"items": ["a", "b"], "done": [], "route": ""})
    assert out["done"] == ["A", "B", "count:2"], out
    updates = list(graph.stream({"items": ["x"], "done": [], "route": ""}, stream_mode="updates"))
    assert updates, "expected stream updates"
    print({"valid": True, "invoke": out, "stream_events": len(updates)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
