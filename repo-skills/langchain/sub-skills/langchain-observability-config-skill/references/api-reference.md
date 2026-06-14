# Observability And Config API Reference

## Runnable Config

Most runnables accept:

```python
config = {
    "tags": ["demo"],
    "metadata": {"component": "retrieval"},
    "run_name": "demo-run",
}
result = chain.invoke(input_data, config=config)
```

## Callbacks

```python
from langchain_core.callbacks import BaseCallbackHandler
```

Pass callbacks through config:

```python
chain.invoke(input_data, config={"callbacks": [handler]})
```

## LangSmith

LangSmith tracing uses the `langsmith` package plus environment variables. Keep tracing optional for smoke tests and avoid logging secrets in inputs, outputs, tags, or metadata.

## Tracers

Tracing utilities live in `langchain_core.tracers`. Prefer documented callback/config entry points before direct tracer usage.
