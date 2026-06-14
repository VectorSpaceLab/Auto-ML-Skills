# Store Runtime Context API Reference

## Store Import

```python
from langgraph.store.memory import InMemoryStore
```

Stores usually operate with namespace tuples and keys. Values should be JSON-serializable or compatible with the selected store backend.

## Store Concepts

- namespace: tuple identifying a memory scope, for example `(user_id, "memories")`
- key: stable item id
- value: payload dict
- search/list/get APIs vary by store but commonly support namespace-based lookup

## Runtime Context

LangGraph has runtime/config concepts for values that should be available during a run but not necessarily stored as graph state. Inspect installed signatures when using advanced runtime context.

## Store vs Checkpoint

- checkpoint: state snapshots for a graph run/thread
- store: cross-run or semantic memory data

Do not use the store as a replacement for reducers/checkpoints in normal graph state updates.
