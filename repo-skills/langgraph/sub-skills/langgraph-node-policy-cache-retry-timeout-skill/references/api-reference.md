# Node Policy API Reference

## Imports

```python
from langgraph.cache.memory import InMemoryCache
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy, RetryPolicy
```

Verified signatures:

```text
StateGraph.add_node(..., defer=False, retry_policy=None, cache_policy=None, error_handler=None, timeout=None, ...)
StateGraph.compile(checkpointer=None, *, cache=None, store=None, interrupt_before=None, interrupt_after=None, debug=False, name=None, ...)
RetryPolicy(initial_interval=0.5, backoff_factor=2.0, max_interval=128.0, max_attempts=3, jitter=True, retry_on=...)
CachePolicy(key_func=default_cache_key, ttl=None)
InMemoryCache(*, serde=None)
```

## Retry

```python
builder.add_node(
    "fetch",
    fetch_node,
    retry_policy=RetryPolicy(max_attempts=3, retry_on=ValueError),
)
```

Keep `retry_on` narrow; broad exception retries can hide logic bugs.

## Cache

```python
builder.add_node("expensive", expensive_node, cache_policy=CachePolicy(ttl=300))
graph = builder.compile(cache=InMemoryCache())
```

Call `graph.clear_cache()` when the compiled graph supports it and cached values must be invalidated.

## Timeout And Defer

Use `timeout` for long-running nodes and `defer=True` for nodes that should run near graph completion. Record side effects before enabling retries or deferred execution.
