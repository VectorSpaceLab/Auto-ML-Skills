#!/usr/bin/env python3
"""No-key sync and async streaming smoke test."""

from __future__ import annotations

import asyncio
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    value: int


def inc(state: State) -> dict:
    return {"value": state["value"] + 1}


async def double(state: State) -> dict:
    await asyncio.sleep(0)
    return {"value": state["value"] * 2}


def build_sync_graph():
    builder = StateGraph(State)
    builder.add_node("inc", inc)
    builder.add_node("inc_again", inc)
    builder.add_edge(START, "inc")
    builder.add_edge("inc", "inc_again")
    builder.add_edge("inc_again", END)
    return builder.compile()


def build_async_graph():
    builder = StateGraph(State)
    builder.add_node("inc", inc)
    builder.add_node("double", double)
    builder.add_edge(START, "inc")
    builder.add_edge("inc", "double")
    builder.add_edge("double", END)
    return builder.compile()


async def async_part(graph) -> dict:
    chunks = []
    async for chunk in graph.astream({"value": 2}, stream_mode="updates"):
        chunks.append(chunk)
    out = await graph.ainvoke({"value": 2})
    return {"chunks": chunks, "out": out}


def main() -> int:
    sync_graph = build_sync_graph()
    async_graph = build_async_graph()
    sync_chunks = list(sync_graph.stream({"value": 1}, stream_mode="updates"))
    async_result = asyncio.run(async_part(async_graph))
    assert sync_chunks, "expected sync stream chunks"
    assert async_result["out"]["value"] == 6, async_result
    print({"valid": True, "sync_chunks": len(sync_chunks), "async_chunks": len(async_result["chunks"])})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
