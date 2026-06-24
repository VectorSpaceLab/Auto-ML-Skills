---
name: langchain-streaming-async-skill
description: "Use when a user wants LangChain streaming, async invocation, batching, abatch, astream, astream_events, concurrency, or stream debugging."
disable-model-invocation: true
---

# LangChain Streaming And Async

Use this sub-skill for stream, batch, async, and event-stream workflows.

## Short Workflow

1. Confirm imports with `../../scripts/check_langchain_env.py`.
2. Read [references/api-reference.md](references/api-reference.md) for sync/async runnable methods.
3. Read [references/workflows.md](references/workflows.md) for streaming, batching, and event handling.
4. Run [scripts/smoke_streaming_async.py](scripts/smoke_streaming_async.py) for deterministic stream and async validation.

## Bundled Scripts

- [scripts/smoke_streaming_async.py](scripts/smoke_streaming_async.py): checks stream, batch, ainvoke, abatch, and astream with a fake model.

## References

- [references/api-reference.md](references/api-reference.md): runnable streaming and async API.
- [references/workflows.md](references/workflows.md): event and concurrency patterns.
- [references/troubleshooting.md](references/troubleshooting.md): async loop, chunk, and rate-limit failures.

## Boundaries

Use models for provider stream capability and observability for traced stream/event runs.
