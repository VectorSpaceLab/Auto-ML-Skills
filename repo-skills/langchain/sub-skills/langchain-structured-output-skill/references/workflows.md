# Structured Output Workflows

## Decision Tree

- If the provider and model support native structured output, use `model.with_structured_output(schema)`.
- If the provider supports tool calling but not strict JSON schema, bind a schema as a tool and parse tool calls.
- If the model only emits text, use prompt instructions plus `JsonOutputParser` or `PydanticOutputParser`.

## Pydantic Schema

```python
class Answer(BaseModel):
    answer: str
    citations: list[str] = []
```

Keep field names stable and descriptions explicit.

## Parser Chain

```python
chain = prompt | model | PydanticOutputParser(pydantic_object=Answer)
```

Inspect raw model text when parsing fails. Add retries or repair logic only after confirming the output shape.

## Include Raw

Some provider implementations support `include_raw=True` for structured output. Use it during debugging to see raw model messages and parsed results together.
