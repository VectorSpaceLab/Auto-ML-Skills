# Functional API Workflows

## Selection Rule

Use functional API when the workflow reads naturally as functions/tasks. Use `StateGraph` when the user needs graph visualization, explicit conditional routing, reducers, subgraphs, or multi-agent handoffs.

## Migration From StateGraph

1. Identify nodes and edges.
2. Convert simple nodes to tasks.
3. Keep branching explicit.
4. Re-run checkpoint and stream tests after migration.

## Persistence

Functional workflows can still need checkpoint/config handling. Preserve `thread_id` and saver setup rules from the persistence sub-skills.
