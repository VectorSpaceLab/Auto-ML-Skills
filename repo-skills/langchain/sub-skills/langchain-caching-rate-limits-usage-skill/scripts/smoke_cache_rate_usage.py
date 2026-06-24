#!/usr/bin/env python3
"""No-key smoke for LangChain cache, rate limiter, and usage metadata."""

from __future__ import annotations

import json


def main() -> int:
    from langchain_core.caches import InMemoryCache
    from langchain_core.callbacks import UsageMetadataCallbackHandler
    from langchain_core.globals import get_llm_cache, set_llm_cache
    from langchain_core.language_models.fake import FakeListLLM
    from langchain_core.messages import AIMessage, UsageMetadata
    from langchain_core.outputs import ChatGeneration, LLMResult
    from langchain_core.rate_limiters import InMemoryRateLimiter

    cache = InMemoryCache(maxsize=8)
    set_llm_cache(cache)
    cached_llm = FakeListLLM(responses=["cold", "should-not-appear"])
    first = cached_llm.invoke("same prompt")
    second = cached_llm.invoke("same prompt")
    global_cache_ok = get_llm_cache() is cache and first == second == "cold" and cached_llm.i == 1

    bypass_llm = FakeListLLM(responses=["first", "second"], cache=False)
    bypass_first = bypass_llm.invoke("same prompt")
    bypass_second = bypass_llm.invoke("same prompt")
    bypass_ok = bypass_first == "first" and bypass_second == "second"

    limiter = InMemoryRateLimiter(
        requests_per_second=1000,
        check_every_n_seconds=0.001,
        max_bucket_size=1,
    )
    rate_first = limiter.acquire(blocking=True)
    rate_second = limiter.acquire(blocking=False)

    cb = UsageMetadataCallbackHandler()
    msg = AIMessage(
        "ok",
        usage_metadata=UsageMetadata(input_tokens=1, output_tokens=2, total_tokens=3),
        response_metadata={"model_name": "fake-model"},
    )
    cb.on_llm_end(LLMResult(generations=[[ChatGeneration(message=msg)]]))
    usage_ok = cb.usage_metadata.get("fake-model", {}).get("total_tokens") == 3
    set_llm_cache(None)

    result = {
        "global_cache_ok": global_cache_ok,
        "bypass_ok": bypass_ok,
        "rate_first": rate_first,
        "rate_second_nonblocking": rate_second,
        "usage_metadata": cb.usage_metadata,
        "usage_ok": usage_ok,
    }
    result["pass"] = bool(global_cache_ok and bypass_ok and rate_first and not rate_second and usage_ok)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
