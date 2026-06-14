# Agents And Tools Workflows

## Safe Tool Definition

- Give every tool precise type hints.
- Add a concise docstring describing behavior and constraints.
- Validate side-effecting tools separately before giving them to an agent.
- Prefer explicit allowlists for file, shell, network, or database operations.

## No-Key Tool Smoke

Use decorated tools directly:

```python
result = add.invoke({"a": 2, "b": 3})
```

Inspect `add.args_schema.model_json_schema()` to verify the model sees the intended schema.

## Agent Construction

```python
agent = create_agent(model=model, tools=[add], system_prompt="Use tools when helpful.")
```

Use live provider agents only after verifying the model supports tool calling. For no-key validation, smoke-test tool schemas and model binding separately.

## Retrieval Tool

Convert retrievers to tools when the model should explicitly decide when to retrieve. Keep retrieval tool outputs short and cite metadata when available.
