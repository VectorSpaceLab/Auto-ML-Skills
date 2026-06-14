# Checkpoint And Interrupt Troubleshooting

- Missing `thread_id`: pass `config={"configurable": {"thread_id": "..."}}` on every checkpointed invoke or stream.
- Interrupt without checkpointer: compile with a checkpointer; interrupts rely on persisted state.
- Duplicate side effects after resume: the interrupted node re-runs. Move side effects after resume or guard them with state.
- Unexpected memory carryover: use a new `thread_id`.
- Lost memory: keep the same checkpointer and `thread_id`, or use a persistent saver instead of process-local memory.
- Postgres tables missing: call `.setup()` before first graph run.
