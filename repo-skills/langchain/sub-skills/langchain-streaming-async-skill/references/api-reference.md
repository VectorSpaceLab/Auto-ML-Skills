# Streaming And Async API Reference

## Runnable Methods

- `invoke(input, config=None)`: one sync result.
- `batch(inputs, config=None)`: sync list of results.
- `stream(input, config=None)`: sync iterator of chunks.
- `ainvoke(input, config=None)`: one async result.
- `abatch(inputs, config=None)`: async list of results.
- `astream(input, config=None)`: async iterator of chunks.
- `astream_events(input, version=..., config=None)`: async iterator of event dictionaries where supported.

## Config

Use runnable config for tracing, tags, metadata, and provider-specific concurrency settings when supported:

```python
config = {"tags": ["stream"], "metadata": {"component": "demo"}}
```

Keep secrets out of config.

## Chunk Types

Chunks can be strings, message chunks, parsed JSON diffs, or event dictionaries depending on the runnable chain.
