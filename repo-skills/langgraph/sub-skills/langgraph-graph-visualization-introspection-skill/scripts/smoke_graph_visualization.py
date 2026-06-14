#!/usr/bin/env python3
"""No-key smoke for LangGraph get_graph, to_json, and Mermaid output."""

from __future__ import annotations

import json
from typing import Literal

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    value: int


def inc(state: State) -> dict[str, int]:
    return {"value": state["value"] + 1}


def route(state: State) -> Literal["finish"]:
    return "finish"


def main() -> int:
    builder = StateGraph(State)
    builder.add_node("inc", inc)
    builder.add_node("finish", lambda state: state)
    builder.add_edge(START, "inc")
    builder.add_conditional_edges("inc", route, path_map={"finish": "finish"})
    builder.add_edge("finish", END)
    graph = builder.compile()

    command_builder = StateGraph(State)
    command_builder.add_node("router", inc, destinations=("finish", END))
    command_builder.add_node("finish", lambda state: state)
    command_builder.add_edge(START, "router")
    command_builder.add_edge("router", "finish")
    command_builder.add_edge("finish", END)
    command_graph = command_builder.compile()

    data = graph.get_graph().to_json()
    mermaid = graph.get_graph().draw_mermaid()
    xray = graph.get_graph(xray=True).to_json()
    command_data = command_graph.get_graph().to_json()
    node_ids = {node["id"] for node in data["nodes"]}
    edge_targets = {edge["target"] for edge in data["edges"]}
    command_node_ids = {node["id"] for node in command_data["nodes"]}
    result = {
        "nodes": sorted(node_ids),
        "edge_targets": sorted(edge_targets),
        "destinations_nodes": sorted(command_node_ids),
        "mermaid_excerpt": mermaid[:160],
        "xray_node_count": len(xray["nodes"]),
    }
    result["pass"] = (
        "inc" in node_ids
        and "finish" in node_ids
        and "finish" in edge_targets
        and "router" in command_node_ids
        and "graph TD" in mermaid
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
