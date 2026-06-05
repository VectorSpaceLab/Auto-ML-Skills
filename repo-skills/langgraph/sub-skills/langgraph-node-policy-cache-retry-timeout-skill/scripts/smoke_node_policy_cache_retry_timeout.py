#!/usr/bin/env python3
"""No-key smoke for LangGraph RetryPolicy, CachePolicy, and clear_cache."""

from __future__ import annotations

import json

from typing_extensions import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import END, START, StateGraph
from langgraph.types import CachePolicy, RetryPolicy


class State(TypedDict):
    x: int
    y: int


def main() -> int:
    counts = {"retry": 0, "cache": 0}

    def flaky(state: State) -> dict[str, int]:
        counts["retry"] += 1
        if counts["retry"] == 1:
            raise ValueError("transient")
        return {"x": state["x"] + 1}

    def cached(state: State) -> dict[str, int]:
        counts["cache"] += 1
        return {"y": state["x"] * 2}

    builder = StateGraph(State)
    builder.add_node(
        "flaky",
        flaky,
        retry_policy=RetryPolicy(max_attempts=2, initial_interval=0, jitter=False, retry_on=ValueError),
    )
    builder.add_node("cached", cached, cache_policy=CachePolicy())
    builder.add_edge(START, "flaky")
    builder.add_edge("flaky", "cached")
    builder.add_edge("cached", END)
    graph = builder.compile(cache=InMemoryCache())

    first = graph.invoke({"x": 1, "y": 0})
    after_first = dict(counts)
    second = graph.invoke({"x": 1, "y": 0})
    after_second = dict(counts)
    graph.clear_cache()
    third = graph.invoke({"x": 1, "y": 0})
    after_clear = dict(counts)

    result = {
        "first": first,
        "second": second,
        "third": third,
        "after_first": after_first,
        "after_second": after_second,
        "after_clear": after_clear,
    }
    result["pass"] = (
        first == {"x": 2, "y": 4}
        and second == first
        and third == first
        and after_first["retry"] == 2
        and after_second["cache"] == after_first["cache"]
        and after_clear["cache"] == after_first["cache"] + 1
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
