# Semantic Store Memory

## Checkpoints Versus Stores

| Need | Use |
| --- | --- |
| Resume one thread exactly where it left off | Checkpointer |
| Share facts across many threads | Store |
| Search remembered facts by namespace | Store |
| Inspect state history/time travel | Checkpointer |

## Namespace Design

Good namespaces are:

- tuple-based
- tenant-scoped
- user-scoped when holding user memory
- stable across runs
- narrow enough to avoid noisy search results

## Value Design

Use compact JSON-like values:

```python
{"text": "prefers terse answers", "kind": "preference", "source": "chat"}
```

Avoid storing large transcripts as one item. Split facts or summaries.

## Search Workflow

1. Pick namespace.
2. Use `search(namespace)` for local store enumeration.
3. If backend has vector index, pass query/filter parameters supported by that backend.
4. Convert returned items into graph context or tool results.

## TTL And Backend Support

Not every backend supports TTL or vector indexes. Check `supports_ttl`, backend docs, and import availability before promising expiry or semantic ranking.
