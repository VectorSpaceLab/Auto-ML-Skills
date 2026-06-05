# Functional API Reference

## Import Surface

```python
import langgraph.func as lg_func
```

Common symbols in recent versions include task/entrypoint-style decorators. Names and signatures can drift, so inspect the installed package before coding.

## Use Cases

- compact workflows where function composition is clearer than explicit graph construction
- task-like steps that may be checkpointed or retried depending on version/runtime
- codebases already using LangGraph functional API patterns

## Caution

Do not assume StateGraph APIs such as `add_edge` exist in functional workflows. Keep thread/checkpoint config visible in user-facing code.
