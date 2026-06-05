# API Reference

## Imports

```python
from langgraph.prebuilt import ToolNode, ValidationNode, create_react_agent, tools_condition
```

## ToolNode

`ToolNode` executes tool calls from one of these inputs:

- State dict with a `messages` key.
- Message list whose last AI message has `tool_calls`.
- Direct tool-call dictionaries.

Output depends on input form. Dict input returns a dict keyed by `messages`; list input returns a list of tool messages.

```python
from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode

def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

node = ToolNode([add])
msg = AIMessage(content="", tool_calls=[{"name": "add", "args": {"a": 1, "b": 2}, "id": "1"}])
out = node.invoke({"messages": [msg]})
```

## tools_condition

`tools_condition(state, messages_key="messages")` returns `"tools"` when the last AI message has tool calls; otherwise it returns `"__end__"`.

Use it with conditional edges:

```python
builder.add_conditional_edges("model", tools_condition, {"tools": "tools", "__end__": END})
```

## create_react_agent

`create_react_agent(model, tools, **kwargs)` creates a compiled tool-calling agent graph. Important kwargs include:

- `prompt`
- `response_format`
- `pre_model_hook`
- `post_model_hook`
- `state_schema`
- `context_schema`
- `checkpointer`
- `store`
- `interrupt_before`
- `interrupt_after`
- `debug`
- `version`

Use a real chat model only when provider packages and credentials are available. For no-key checks, validate graph construction separately or use `ToolNode` direct calls.

## Injected Args

`ToolNode` supports injected state/store patterns for tools that need graph context but should not expose that argument to the model. Keep injected dependencies deterministic in tests.
