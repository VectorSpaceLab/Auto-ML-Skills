# Structured Output API Reference

## Native Structured Output

Many chat models expose:

```python
structured_model = model.with_structured_output(MySchema)
```

`MySchema` can often be a Pydantic model, JSON schema, TypedDict, or provider-compatible tool schema. Behavior varies by provider.

## Parser-Based Structured Output

```python
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
```

`PydanticOutputParser(pydantic_object=MyModel)` validates JSON text into a Pydantic object.

## Tool And Function Parsers

OpenAI-style tool/function parsers live under `langchain_core.output_parsers.openai_tools` and `langchain_core.output_parsers.openai_functions`.

Use them when the model response contains tool calls or function-call arguments rather than plain JSON text.
