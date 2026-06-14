---
name: vllm-structured-outputs
description: "Use when a user wants vLLM structured outputs, guided decoding, JSON schema, regex, choice, grammar constraints, tool calling, or reasoning-output request patterns."
disable-model-invocation: true
---

# vLLM Structured Outputs

Use this sub-skill for constrained generation and tool/reasoning request payloads. It covers JSON schema, regex, choices, grammar constraints, guided decoding fields, tool calling, and reasoning-output request patterns.

## Use When

- The user wants JSON-mode, JSON schema, regex, grammar, choices, or deterministic machine-parseable output.
- The user asks for OpenAI-compatible structured output payloads or offline guided decoding examples.
- The user wants tool-call or reasoning-output request patterns through vLLM.
- The user needs to debug invalid schema, unsupported constraint fields, or malformed generated JSON.

## Inputs To Collect

- Desired output format, endpoint family, model, prompt, schema/regex/grammar, strictness, parser expectations, and max token budget.
- Whether the route is offline Python, `/v1/chat/completions`, `/v1/completions`, or `/v1/responses`.
- Whether tools or reasoning fields are part of the request.

## Short Workflow

1. Identify whether the user needs JSON schema, regex, choices, grammar, tool calls, or reasoning output parsing.
2. Read [references/workflows.md](references/workflows.md) for offline and server paths.
3. Read [references/guided-decoding.md](references/guided-decoding.md) for supported payload fields and backend caveats.
4. Validate schemas locally before sending to vLLM; simplify complex schemas when decoding fails.
5. Smoke with small `max_tokens`, deterministic temperature, and a prompt that matches the schema.
6. Parse the actual response with the downstream parser before calling the workflow successful.

## Bundled Scripts

- [scripts/make_structured_payload.py](scripts/make_structured_payload.py): creates chat/completion payloads with JSON schema, regex, or choices.
- [scripts/validate_schema.py](scripts/validate_schema.py): validates JSON schema syntax and writes a compact report.

## References

- [references/workflows.md](references/workflows.md): structured-output workflow and output inspection.
- [references/guided-decoding.md](references/guided-decoding.md): guided decoding fields, examples, and pitfalls.

## Boundaries

Use `vllm-openai-serving` for server lifecycle and `vllm-offline-inference` for general generation without constraints.

## Verification Notes

- Schema validation is static; it does not prove the model followed the schema.
- Real validation requires sending the payload to vLLM and parsing the returned content.
- Keep the prompt and schema small for first smoke, then expand.
