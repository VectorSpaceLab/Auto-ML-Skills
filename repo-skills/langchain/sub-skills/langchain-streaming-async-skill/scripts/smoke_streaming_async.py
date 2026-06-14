#!/usr/bin/env python3
"""No-key smoke test for LangChain streaming and async APIs."""

from __future__ import annotations

import asyncio
import json


async def async_part(model):
    ainvoke = await model.ainvoke("x")
    abatch = await model.abatch(["a", "b"])
    chunks = []
    async for chunk in model.astream("y"):
        chunks.append(getattr(chunk, "content", str(chunk)))
    return ainvoke.content, [item.content for item in abatch], chunks


def main() -> int:
    from langchain_core.language_models import FakeListChatModel

    model = FakeListChatModel(responses=["one", "two", "three", "four", "five"])
    stream_chunks = [getattr(chunk, "content", str(chunk)) for chunk in model.stream("s")]
    batch_values = [msg.content for msg in model.batch(["a", "b"])]
    async_invoke, async_batch, async_chunks = asyncio.run(async_part(model))
    result = {
        "stream_chunks": stream_chunks,
        "batch": batch_values,
        "async_invoke": async_invoke,
        "async_batch": async_batch,
        "async_chunks": async_chunks,
    }
    result["pass"] = bool(stream_chunks) and len(batch_values) == 2 and bool(async_invoke) and len(async_batch) == 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
