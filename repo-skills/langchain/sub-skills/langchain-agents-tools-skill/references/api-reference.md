# Agents And Tools API Reference

## Modern Agent Factory

```python
from langchain.agents import create_agent
```

`create_agent` constructs a modern agent around a chat model and tools. Exact runtime behavior depends on the installed LangChain version and provider/tool-calling support.

## Tools

```python
from langchain_core.tools import tool, StructuredTool, BaseTool
```

Define tools with type hints and docstrings:

```python
@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b
```

The decorated object exposes a name, description, args schema, and `.invoke(...)`.

## Tool Binding

Many chat model integrations support:

```python
model_with_tools = model.bind_tools([add])
```

Provider support varies. Some providers require tool-choice configuration or specific model names.

## Tool Conversion

Function calling helpers live under `langchain_core.utils.function_calling` and are useful for inspecting schemas, but do not depend on private provider conversion code.
