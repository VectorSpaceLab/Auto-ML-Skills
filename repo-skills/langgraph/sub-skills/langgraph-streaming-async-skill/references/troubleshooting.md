# Streaming Troubleshooting

- `graph.stream()` returns an iterator; consume it once or create a new run.
- Use `async for` with `astream`; do not wrap it in `list()` outside an event loop.
- A graph containing async-only nodes must be run through `ainvoke` or `astream`; sync `invoke` and `stream` cannot execute async-only nodes.
- `messages` mode is useful for LLM token chunks, not simple deterministic nodes.
- Large `values` snapshots can be expensive; use `updates` for long-running graphs.
- Include `subgraphs=True` when nested graph event provenance matters.
- Streaming with checkpoints still needs `configurable.thread_id`.
