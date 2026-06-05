---
name: vllm-structured-outputs
description: "Use when a user wants vLLM structured outputs, guided decoding, JSON schema, regex, choice, grammar constraints, tool calling, or reasoning-output request patterns."
disable-model-invocation: true
---

# vLLM Structured Outputs

Use this sub-skill for constrained generation and tool/reasoning request payloads.

## Short Workflow

1. Identify whether the user needs JSON schema, regex, choices, grammar, tool calls, or reasoning output parsing.
2. Read [references/workflows.md](references/workflows.md) for offline and server paths.
3. Read [references/guided-decoding.md](references/guided-decoding.md) for supported payload fields and backend caveats.
4. Validate schemas locally before sending to vLLM; simplify complex schemas when decoding fails.
5. Smoke with small `max_tokens`, deterministic temperature, and a prompt that matches the schema.

## Bundled Scripts

- [scripts/make_structured_payload.py](scripts/make_structured_payload.py): creates chat/completion payloads with JSON schema, regex, or choices.
- [scripts/validate_schema.py](scripts/validate_schema.py): validates JSON schema syntax and writes a compact report.

## References

- [references/workflows.md](references/workflows.md): structured-output workflow and output inspection.
- [references/guided-decoding.md](references/guided-decoding.md): guided decoding fields, examples, and pitfalls.

## Boundaries

Use `vllm-openai-serving` for server lifecycle and `vllm-offline-inference` for general generation without constraints.
