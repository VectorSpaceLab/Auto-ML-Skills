# Persistence Backends Troubleshooting

- Missing backend module: install the optional checkpoint package.
- Missing `thread_id`: every checkpointed call needs configurable `thread_id`.
- State not durable: `InMemorySaver` is process-local; use SQLite/Postgres.
- Postgres relation/table missing: call `.setup()`.
- Async graph with sync saver: use async saver classes where required.
- Connection leaks: use context managers or explicit close methods supported by the saver.
- Confusing memory carryover: change `thread_id` for a fresh run.
