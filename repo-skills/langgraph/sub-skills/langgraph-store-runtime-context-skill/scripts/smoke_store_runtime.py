#!/usr/bin/env python3
"""No-key smoke test for LangGraph InMemoryStore."""

from __future__ import annotations

from langgraph.store.memory import InMemoryStore


def main() -> int:
    store = InMemoryStore()
    ns = ("user-1", "memories")
    store.put(ns, "fact-1", {"text": "likes concise answers"})
    item = store.get(ns, "fact-1")
    found = store.search(ns)
    ok = item is not None and len(found) >= 1
    print({"valid": ok, "item": getattr(item, "value", None), "found": len(found)})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
