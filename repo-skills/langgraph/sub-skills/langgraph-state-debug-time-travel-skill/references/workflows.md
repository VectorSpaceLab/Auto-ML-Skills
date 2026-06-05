# State Debug Time Travel Workflows

## Inspect Current State

1. Reproduce with the same checkpointer and `thread_id`.
2. Call `get_state(config)`.
3. Inspect values, next tasks, metadata, and checkpoint config.

## Time Travel

1. Call `get_state_history(config)`.
2. Select the checkpoint before the bad transition.
3. Resume or branch from that checkpoint according to installed API behavior.
4. Record the checkpoint id/config in the report.

## Repair State

1. Stop active runs for that thread.
2. Call `update_state` with minimal values.
3. Use `as_node` when the update should be attributed to a node.
4. Re-run downstream nodes and compare output.
