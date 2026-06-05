# ToolNode Interceptors

## `wrap_tool_call`

`ToolNode(..., wrap_tool_call=wrapper)` lets code inspect, modify, short-circuit, or handle a tool call around normal execution.

Run wrappers inside a compiled graph for reliable runtime context:

```python
tool_node = ToolNode([tool], wrap_tool_call=wrapper)
```

The wrapper receives a request object and an execute callback in current versions. Inspect the installed signature/tests before depending on request internals.

## Error Handling

`ToolNode` also accepts `handle_tool_errors`, which can be:

- boolean
- string
- callable
- exception type or tuple

Keep error messages safe to expose to the model.

## Injected State And Store

Use `InjectedState` and `InjectedStore` when tools need graph internals that should not appear in the tool schema shown to the model.

## Runtime Boundary

Direct `ToolNode.invoke()` may miss required runtime config. Prefer compiled `StateGraph` smoke tests.
