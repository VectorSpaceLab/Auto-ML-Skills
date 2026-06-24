# Persistence Backends API Reference

## Memory

```python
from langgraph.checkpoint.memory import InMemorySaver
```

`InMemorySaver` is process-local. It is good for tests and demos, not restart persistence.

## SQLite

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
```

Install `langgraph-checkpoint-sqlite`. Use SQLite for local persistence and development.

## Postgres

```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
```

Install `langgraph-checkpoint-postgres`. Use Postgres for shared durable persistence. Call `.setup()` before first use.

## Required Runtime Config

Checkpointed runs require:

```python
config = {"configurable": {"thread_id": "stable-id"}}
```

Reuse `thread_id` to continue a run; change it to isolate runs.
