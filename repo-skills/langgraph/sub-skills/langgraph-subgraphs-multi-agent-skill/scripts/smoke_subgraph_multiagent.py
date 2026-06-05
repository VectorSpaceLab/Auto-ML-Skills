#!/usr/bin/env python3
"""No-key smoke test for subgraphs and dynamic fan-out."""

from __future__ import annotations

import operator
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ChildState(TypedDict):
    text: str
    result: str


def child_node(state: ChildState) -> dict:
    return {"result": state["text"].strip().upper()}


def build_child():
    builder = StateGraph(ChildState)
    builder.add_node("normalize", child_node)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", END)
    return builder.compile()


class ParentState(TypedDict):
    items: list[str]
    results: Annotated[list[str], operator.add]


class WorkerState(TypedDict):
    text: str


def fan_out(state: ParentState):
    return [Send("worker", {"text": item}) for item in state["items"]]


def collect(state: ChildState) -> dict:
    return {"results": [state["result"]]}


def main() -> int:
    child = build_child()
    parent = StateGraph(ParentState)
    parent.add_node("worker", lambda state: {"results": [child.invoke({"text": state["text"], "result": ""})["result"]]})
    parent.add_conditional_edges(START, fan_out)
    parent.add_edge("worker", END)
    graph = parent.compile()
    out = graph.invoke({"items": [" a ", "b"], "results": []})
    assert out["results"] == ["A", "B"], out
    print({"valid": True, "results": out["results"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
