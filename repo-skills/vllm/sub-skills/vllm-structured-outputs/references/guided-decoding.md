# Guided Decoding Reference

## Request Fields

Current vLLM versions support guided/structured output through OpenAI-compatible extra fields and `SamplingParams` fields. Common concepts:

- JSON schema object constraints.
- Regex constraints.
- Choice constraints.
- Grammar constraints.
- Backend choice such as xgrammar or guidance when available.

Field names vary across versions. Validate with `inspect_api.py` and a minimal request before production.

## JSON Schema Tips

- Keep schema shallow for first smoke.
- Include `required` fields.
- Avoid broad `anyOf`/`oneOf`/recursive schemas for initial tests.
- Set `max_tokens` high enough for full JSON.
- Keep prompt aligned with schema names.

## Example Payload

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "messages": [{"role": "user", "content": "Return a city and country as JSON."}],
  "guided_json": {
    "type": "object",
    "properties": {
      "city": {"type": "string"},
      "country": {"type": "string"}
    },
    "required": ["city", "country"]
  },
  "temperature": 0,
  "max_tokens": 64
}
```
