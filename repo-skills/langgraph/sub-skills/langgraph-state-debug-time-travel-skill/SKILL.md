---
name: langgraph-state-debug-time-travel-skill
description: "Use when a user wants LangGraph state inspection, get_state, get_state_history, update_state, time travel, replay, debugging, recursion limits, or checkpoint repair workflows."
disable-model-invocation: true
---

# LangGraph State Debug Time Travel

Use `langgraph-state-debug-time-travel-skill` when the main task is observing, repairing, replaying, or time-traveling graph state. Quick answer: compile with a checkpointer, use `get_state`, `get_state_history`, and `update_state`, and validate with `scripts/smoke_state_debug.py`.

## Short Workflow

1. Ensure the graph is compiled with a checkpointer and invoked with `thread_id`.
2. Use `get_state(config)` for the current snapshot.
3. Use `get_state_history(config)` for checkpoint history/time travel.
4. Use `update_state(config, values, as_node=...)` only with an audit trail.
5. For recursion/loop issues, inspect route decisions and set/adjust recursion limits through config.
6. Run [scripts/smoke_state_debug.py](scripts/smoke_state_debug.py).

## Bundled Scripts

- [scripts/smoke_state_debug.py](scripts/smoke_state_debug.py): no-key checkpointed graph smoke for `get_state`, history, and `update_state`.

## References

- [references/api-reference.md](references/api-reference.md): state inspection methods and config shape.
- [references/workflows.md](references/workflows.md): replay, repair, time travel, and debug patterns.
- [references/troubleshooting.md](references/troubleshooting.md): missing history, wrong thread, loops, and unsafe updates.

## Boundaries

Use checkpoint/interrupt skill for human pause/resume and persistence backend skill for saver setup.
