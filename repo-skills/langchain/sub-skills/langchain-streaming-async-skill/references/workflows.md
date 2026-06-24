# Streaming And Async Workflows

## Sync Streaming

```python
for chunk in chain.stream(input_data):
    handle(chunk)
```

For chat models, inspect `chunk.content` when chunks are message chunks.

## Async Streaming

```python
async for chunk in chain.astream(input_data):
    handle(chunk)
```

Do not wrap this in `asyncio.run` inside an already running event loop.

## Batch

```python
results = chain.batch(inputs)
results = await chain.abatch(inputs)
```

Use smaller batches or provider concurrency controls when rate limits appear.

## Event Streams

Use `astream_events` when debugging nested chains, callbacks, and tool calls. Event payloads are dictionaries; log event names and run IDs but avoid secrets in input/output logs.
