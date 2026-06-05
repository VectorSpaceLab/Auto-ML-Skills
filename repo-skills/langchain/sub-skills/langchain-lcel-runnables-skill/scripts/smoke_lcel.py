#!/usr/bin/env python3
"""No-key smoke test for LangChain LCEL runnables."""

from __future__ import annotations

import asyncio
import json


async def async_check(chain):
    return await chain.ainvoke("async")


def main() -> int:
    from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

    strip = RunnableLambda(lambda x: x.strip())
    upper = RunnableLambda(lambda x: x.upper())
    chain = strip | upper
    sequence = chain.invoke(" ok ")
    batch = chain.batch([" a ", " b "])
    parallel = RunnableParallel(raw=RunnablePassthrough(), upper=upper).invoke("hi")
    assigned = RunnablePassthrough.assign(length=lambda x: len(x["text"])).invoke({"text": "hello"})

    def fail(_):
        raise ValueError("primary failed")

    fallback = RunnableLambda(fail).with_fallbacks([RunnableLambda(lambda _: "fallback")]).invoke("x")
    async_result = asyncio.run(async_check(chain))
    result = {
        "sequence": sequence,
        "batch": batch,
        "parallel": parallel,
        "assigned": assigned,
        "fallback": fallback,
        "async": async_result,
    }
    result["pass"] = (
        sequence == "OK"
        and batch == ["A", "B"]
        and parallel == {"raw": "hi", "upper": "HI"}
        and assigned == {"text": "hello", "length": 5}
        and fallback == "fallback"
        and async_result == "ASYNC"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
