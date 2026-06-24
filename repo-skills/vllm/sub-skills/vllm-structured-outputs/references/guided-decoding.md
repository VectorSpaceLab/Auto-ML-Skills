# Guided Decoding Reference

## Request Fields

Current vLLM versions support guided/structured output through OpenAI-compatible extra fields and `SamplingParams` fields. Common concepts:

- JSON schema object constraints.
- Regex constraints.
- Choice constraints.
- Grammar constraints.
- Backend choice such as `xgrammar` or `guidance` when available.

Field names vary across versions. Validate with `inspect_api.py` and a minimal request before production. Newer OpenAI-compatible requests commonly accept a nested `structured_outputs` object through `extra_body`; older payloads may use `guided_json`, `guided_regex`, or `guided_choice` directly.

## Backend Selection

Server-level backend configuration is version-sensitive. Check `vllm serve --help` or `scripts/inspect_api.py` for:

- `--structured-outputs-config '<json>'`
- legacy guided decoding backend flags, if present
- per-request `structured_outputs` fields

Use the default backend first. Switch backend only when the target schema/grammar requires it or a benchmark shows the default is too slow.

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

Nested extra-body form:

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "messages": [{"role": "user", "content": "Return a city and country as JSON."}],
  "structured_outputs": {
    "json": {
      "type": "object",
      "properties": {
        "city": {"type": "string"},
        "country": {"type": "string"}
      },
      "required": ["city", "country"]
    }
  },
  "temperature": 0,
  "max_tokens": 64
}
```

## Tool Calling

Tool calling is model-, parser-, and chat-template-specific. For automatic tool choice, the server usually needs both:

```bash
vllm serve MODEL --enable-auto-tool-choice --tool-call-parser PARSER
```

Common parser names are model-family-specific, such as Llama JSON variants, Mistral, Hermes, Granite, GLM, DeepSeek, Qwen3 Coder, Pythonic parsers, and other parsers exposed by the installed package. If a tool call comes back as plain text, check:

- the model was instruction/tool tuned
- the chat template includes tool rendering
- `--tool-call-parser` matches the model family
- `tool_choice`, `parallel_tool_calls`, and required-tool settings are compatible with the model

Responses API tool payloads are similar in concept but use the Responses request schema. Smoke both `/v1/chat/completions` and `/v1/responses` separately when both are required.

## Reasoning Parsers

Reasoning output parsing is separate from tool parsing:

```bash
vllm serve MODEL --reasoning-parser PARSER
```

Parser support depends on the model family and installed version. Use examples with tiny `max_tokens` first and verify where reasoning text appears in the response object. Reasoning models may require a custom chat template or model-specific request fields.
