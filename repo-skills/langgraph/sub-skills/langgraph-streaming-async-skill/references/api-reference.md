# API Reference

## Sync Streaming

```python
for chunk in graph.stream(inputs, stream_mode="updates"):
    print(chunk)
```

`stream_mode` can be a string or a list of modes. Common modes:

- `values`
- `updates`
- `messages`
- `debug`
- `tasks`
- `custom`

## Async Streaming

```python
async for chunk in graph.astream(inputs, stream_mode="values"):
    ...
```

Use `ainvoke` for async final outputs.

## Event Streaming

`stream_events` and `astream_events` expose richer event objects and versioned event APIs. Use these when the user needs metadata, namespaces, lifecycle events, or custom transformers.

```python
for event in graph.stream_events(inputs, version="v2"):
    ...
```

Some versions support higher-level run objects for built-in event projections. Check current signatures with `scripts/inspect_langgraph_api.py --summary`.

## Subgraph Namespaces

Pass `subgraphs=True` when the user needs to distinguish events from nested graphs. Namespaces identify which graph or subgraph emitted an event.
