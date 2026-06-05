#!/usr/bin/env python3
"""No-key smoke for LangGraph InMemoryStore long-term memory operations."""

from __future__ import annotations

import json

from langgraph.store.memory import InMemoryStore


def main() -> int:
    store = InMemoryStore()
    namespace = ("users", "u1", "memories")
    store.put(namespace, "fact-1", {"text": "likes concise answers", "kind": "preference"})
    store.put(namespace, "fact-2", {"text": "works with LangGraph", "kind": "work"})
    item = store.get(namespace, "fact-1")
    hits = store.search(namespace)
    namespaces = store.list_namespaces()
    store.delete(namespace, "fact-2")
    after_delete = store.search(namespace)

    result = {
        "item_value": item.value if item else None,
        "hit_count": len(hits),
        "namespaces": [list(ns) for ns in namespaces],
        "after_delete_count": len(after_delete),
    }
    result["pass"] = (
        result["item_value"] == {"text": "likes concise answers", "kind": "preference"}
        and result["hit_count"] == 2
        and list(namespace) in result["namespaces"]
        and result["after_delete_count"] == 1
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
