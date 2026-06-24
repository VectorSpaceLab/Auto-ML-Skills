---
name: langgraph-semantic-store-memory-skill
description: "Use when a user wants LangGraph long-term memory, semantic store, BaseStore, InMemoryStore search, namespaces, cross-thread memory, TTL, vector store memory, or store backend troubleshooting."
disable-model-invocation: true
---

# LangGraph Semantic Store Memory

Use `langgraph-semantic-store-memory-skill` for long-term memory stored outside checkpoint state. Quick answer: checkpoints store per-thread short-term graph state by `thread_id`; `InMemoryStore` stores cross-thread long-term memory; choose a namespace tuple such as `("users", user_id, "memories")`; validate `put/get/search/list_namespaces` with [scripts/smoke_store_search_memory.py](scripts/smoke_store_search_memory.py).

Minimum answer checklist: name `langgraph-semantic-store-memory-skill`, `scripts/smoke_store_search_memory.py`, `InMemoryStore`, `namespace`, `checkpoint`, and cross-thread memory.

## Short Workflow

1. Separate checkpoint memory from store memory:
   - checkpoints: current graph state by `thread_id`
   - store: long-term facts/searchable records across threads
2. Start with `InMemoryStore` for no-key tests.
3. Design namespace tuples such as `("users", user_id, "memories")`.
4. Store values as small JSON-like dictionaries with stable keys.
5. Use `search()` for namespace-local lookup and optional backend vector search when configured.
6. Run [scripts/smoke_store_search_memory.py](scripts/smoke_store_search_memory.py).

## Bundled Scripts

- [scripts/smoke_store_search_memory.py](scripts/smoke_store_search_memory.py): validates `put`, `get`, `search`, `delete`, and `list_namespaces` on `InMemoryStore`.
- [scripts/check_store_backends.py](scripts/check_store_backends.py): import-checks optional SQLite/Postgres store packages without opening external DBs.

## References

- [references/semantic-store.md](references/semantic-store.md): namespace, value, search, TTL, and vector index guidance.
- [references/api-reference.md](references/api-reference.md): store public imports and methods.
- [references/troubleshooting.md](references/troubleshooting.md): namespace mistakes, checkpoint/store confusion, optional backend issues.

## Boundaries

Use store/runtime context skill for compile-time runtime/store injection. Use persistence backends for checkpoint savers. Use this skill for memory records and store search.
