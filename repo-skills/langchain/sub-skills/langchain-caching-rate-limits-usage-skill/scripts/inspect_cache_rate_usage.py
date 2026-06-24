#!/usr/bin/env python3
"""Inspect LangChain cache, rate limiter, and usage callback APIs."""

from __future__ import annotations

import importlib
import inspect
import json


TARGETS = [
    "langchain_core.caches.InMemoryCache",
    "langchain_core.globals.set_llm_cache",
    "langchain_core.globals.get_llm_cache",
    "langchain_core.rate_limiters.InMemoryRateLimiter",
    "langchain_core.callbacks.UsageMetadataCallbackHandler",
    "langchain_core.callbacks.get_usage_metadata_callback",
    "langchain_core.language_models.fake.FakeListLLM",
    "langchain_core.language_models.fake_chat_models.FakeListChatModel",
]


def inspect_target(target: str) -> dict[str, object]:
    modname, attr = target.rsplit(".", 1)
    try:
        obj = getattr(importlib.import_module(modname), attr)
        return {"target": target, "ok": True, "signature": str(inspect.signature(obj))}
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        return {"target": target, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    rows = [inspect_target(target) for target in TARGETS]
    result = {"targets": rows, "pass": all(row["ok"] for row in rows)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
