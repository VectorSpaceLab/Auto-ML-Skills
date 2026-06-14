---
name: langgraph-persistence-backends-skill
description: "Use when a user wants LangGraph checkpoint persistence backends, InMemorySaver, SQLite, Postgres, async savers, setup, thread_id persistence, or backend troubleshooting."
disable-model-invocation: true
---

# LangGraph Persistence Backends

Use `langgraph-persistence-backends-skill` when the checkpointer choice or backend setup is the main task. Quick answer: `InMemorySaver` for tests, `langgraph-checkpoint-sqlite` for local durable persistence, `langgraph-checkpoint-postgres` for shared production persistence, always pass `thread_id`, and validate with `scripts/check_persistence_backends.py`.

## Short Workflow

1. Pick backend by durability target: memory, SQLite, or Postgres.
2. Install optional backend packages only when needed.
3. Compile with `builder.compile(checkpointer=saver)`.
4. Pass `config={"configurable": {"thread_id": "..."}}` on every invoke/stream.
5. For Postgres, call saver `.setup()` before first use.
6. Read [references/api-reference.md](references/api-reference.md), then run [scripts/check_persistence_backends.py](scripts/check_persistence_backends.py).

## Bundled Scripts

- [scripts/check_persistence_backends.py](scripts/check_persistence_backends.py): import-checks memory, SQLite, Postgres, and async saver classes without opening DB connections.
- [scripts/smoke_inmemory_persistence.py](scripts/smoke_inmemory_persistence.py): no-key checkpoint persistence smoke with `InMemorySaver` and `thread_id`.

## References

- [references/api-reference.md](references/api-reference.md): saver imports, setup requirements, and config keys.
- [references/workflows.md](references/workflows.md): backend selection and migration patterns.
- [references/troubleshooting.md](references/troubleshooting.md): missing packages, thread ids, setup, connection, and async issues.

## Boundaries

Use `langgraph-checkpoint-interrupt-skill` for interrupt/resume behavior; use this skill for backend selection and operations.
