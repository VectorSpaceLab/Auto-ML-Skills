---
name: langgraph-streaming-async-skill
description: "Use when a user wants LangGraph stream, astream, stream_mode values or updates or messages or debug or tasks, stream_events, astream_events, async graph execution, custom streaming, or subgraph stream namespaces."
disable-model-invocation: true
---

# LangGraph Streaming Async

Use this sub-skill for output streaming, event streaming, async graph execution, and stream debugging.

## Short Workflow

1. Build and compile the graph.
2. Select stream mode:
   - `values`: full state snapshots.
   - `updates`: per-node state updates.
   - `messages`: LLM token/message chunks.
   - `debug`: detailed runtime debug events.
   - `tasks`: task lifecycle, useful for subgraphs and observability.
3. Use `graph.stream(..., stream_mode=...)` for sync code.
4. Use `async for event in graph.astream(..., stream_mode=...)` for async code.
5. Use `stream_events` or `astream_events` when event-level metadata is required.
6. Add `subgraphs=True` when subgraph namespaces should be included.
7. Run [scripts/smoke_streaming_async.py](scripts/smoke_streaming_async.py).

## References

- [references/api-reference.md](references/api-reference.md): stream methods, stream modes, async patterns, and event notes.
- [references/workflows.md](references/workflows.md): UI streaming, debug streaming, async tests, and subgraph streams.
- [references/troubleshooting.md](references/troubleshooting.md): stream consumption and mode pitfalls.

## Bundled Scripts

- [scripts/smoke_streaming_async.py](scripts/smoke_streaming_async.py): no-key sync and async stream smoke.

## Boundaries

Use `langgraph-platform-cli-skill` for server streaming over deployed APIs. Use this sub-skill for local compiled graph runtime streams.
