# State Debug Time Travel API Reference

Compiled graph methods commonly include:

- `get_state(config)`: current state snapshot for a checkpointed thread.
- `get_state_history(config)`: iterable/list of checkpoint snapshots.
- `update_state(config, values, as_node=...)`: manually update state at a checkpoint.
- stream with `stream_mode="debug"` or `stream_mode="tasks"` for runtime traces.

Required config:

```python
config = {"configurable": {"thread_id": "stable-id"}}
```

Manual state updates should be logged with reason, operator, before/after values, and downstream rerun plan.
