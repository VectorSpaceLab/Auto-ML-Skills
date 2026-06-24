# Semantic Store API Reference

## Imports

```python
from langgraph.store.memory import InMemoryStore
```

Some installed versions also expose store types through checkpoint/backend packages.

## Basic Methods

```python
store = InMemoryStore()
store.put(("users", "u1"), "fact-1", {"text": "likes concise answers"})
item = store.get(("users", "u1"), "fact-1")
hits = store.search(("users", "u1"))
namespaces = store.list_namespaces()
store.delete(("users", "u1"), "fact-1")
```

Async counterparts include `aput`, `aget`, `asearch`, `adelete`, and `alist_namespaces`.

## Namespace Shape

Namespaces are tuples. Use stable hierarchy:

```python
("tenant", tenant_id, "users", user_id, "memories")
```

## Store Items

Store returns item objects with fields such as:

- `namespace`
- `key`
- `value`
- `created_at`
- `updated_at`
- optional `score`

## Vector/TTL Boundary

Vector indexing and TTL depend on the store backend and index configuration. Validate backend-specific support before relying on semantic search or expiry.
