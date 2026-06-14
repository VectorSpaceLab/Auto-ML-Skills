# Persistence Backend Workflows

## Test/Demo Memory

1. `saver = InMemorySaver()`.
2. Compile graph with `checkpointer=saver`.
3. Invoke twice with same `thread_id` and confirm state persists.

## Local SQLite

1. Install `langgraph-checkpoint-sqlite`.
2. Create saver through the documented constructor/context manager for the installed version.
3. Store DB path outside temporary directories if persistence matters.
4. Use async saver for async graph execution.

## Production Postgres

1. Install `langgraph-checkpoint-postgres`.
2. Configure connection string or connection object without printing credentials.
3. Call `.setup()` once before first run.
4. Use unique `thread_id` for independent users/runs.
5. Monitor connection pooling and transaction behavior.
