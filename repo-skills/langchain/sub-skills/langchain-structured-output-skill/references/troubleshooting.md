# Structured Output Troubleshooting

- `with_structured_output` missing: use a different provider package/model or parser-based extraction.
- Pydantic validation fails: compare raw output with required fields and types.
- Model emits markdown fences: strip or prompt against fences before JSON parsing.
- Tool-call parser sees no tool calls: verify model was bound to tools and tool calling is supported.
- Provider strict mode fails: reduce schema complexity and check provider-specific restrictions.
