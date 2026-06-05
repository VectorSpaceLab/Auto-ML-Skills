# Workflows

## UI State Updates

Use `stream_mode="updates"` to update UI panels per node. This is usually more compact than full state snapshots.

## State Snapshot Debugging

Use `stream_mode="values"` to see complete state after supersteps. This is useful for reducer and routing bugs.

## Token Streaming

Use `stream_mode="messages"` for model token or message chunks. Deterministic Python nodes do not emit meaningful token chunks.

## Async Service Integration

1. Make async nodes `async def`.
2. Compile normally.
3. Use `await graph.ainvoke(...)` or `async for item in graph.astream(...)`.
4. Keep blocking IO out of async nodes.

## Subgraph Observability

Use `stream_mode=["updates", "tasks"]` and `subgraphs=True` to trace nested graph behavior. Add stable node names so emitted events are easier to interpret.
