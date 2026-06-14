# Workflows

## Conversation Memory

1. Define a state with `messages: Annotated[list, add_messages]`.
2. Compile with a checkpointer.
3. Invoke every turn with the same `thread_id`.
4. Inspect state to confirm messages persist.

## Human Approval

1. Put `interrupt(request_payload)` in an approval node.
2. Return the human decision in a later state update.
3. Resume with `Command(resume=response)`.
4. Route based on the resumed value using `Command(goto=...)` or conditional edges.

## SQLite Local Persistence

Use SQLite when memory should survive process restarts but the workflow remains local. Install the SQLite checkpointer package and use the documented saver context manager.

## Postgres Persistence

Use Postgres for shared durable persistence. Install the Postgres checkpointer package, create the saver from a connection string or connection, and call `.setup()` once before first use. For async workflows use `AsyncPostgresSaver`.

## Time Travel And State Fixes

1. Use `get_state_history(config)` to list checkpoints.
2. Select a checkpoint config.
3. Resume from or update state at that checkpoint depending on the user's goal.
4. Keep a clear audit log of manual `update_state` calls.
