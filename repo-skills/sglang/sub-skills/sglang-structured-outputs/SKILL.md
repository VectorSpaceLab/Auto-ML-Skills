---
name: sglang-structured-outputs
description: "Configure SGLang JSON schema, regex, EBNF, structural tags, choices, and constrained decoding."
disable-model-invocation: true
---

# SGLang Structured Outputs

Use this sub-skill for JSON schema, regex, EBNF, structural tags, constrained decoding backends, frontend choices/select, and validation of request payloads. It is the right entry point when the user needs machine-parseable output rather than best-effort formatting.

Read [references/structured-outputs.md](references/structured-outputs.md) for native sampling fields, frontend patterns, OpenAI-compatible behavior, and failure modes. Use [scripts/validate_constraints.py](scripts/validate_constraints.py) to check mutual exclusivity and schema/regex syntax before runtime.

## Use When

- The user wants JSON objects, enum/choice outputs, regex formats, EBNF grammar, structural tags, or constrained decoding.
- The user asks why SGLang rejects a payload with multiple constraint fields.
- The user wants to combine structured output with tools, reasoning parsers, or chat templates.
- The user needs a minimal validation path before running a model.

## Inputs To Collect

- Desired output schema/format, endpoint family, prompt, model, strictness requirements, and downstream parser expectations.
- Constraint type: `json_schema`, `regex`, `ebnf`, `structural_tag`, `choices`, or frontend `sgl.select`.
- Whether the route is native `/generate`, language frontend, OpenAI chat, or Responses API.

## Workflow

1. Pick one constraint mechanism: JSON schema for objects, regex for compact lexical formats, EBNF for grammar, structural tags for tool-style sections, or choices for classification.
2. Validate the constraint locally before sending requests.
3. Use native `/generate` or language frontend for SGLang-specific constraint fields; OpenAI-compatible routes can carry response-format/tool fields when supported by the server parser.
4. For reasoning models with hidden thinking, route combined questions to `sglang-tool-reasoning`.
5. Keep smoke outputs short and deterministic; simplify the schema before debugging model quality.

## Verification

- Run the validator script first; it catches invalid JSON schema and mutually exclusive constraints.
- For a real smoke, use a small prompt and parse the returned text with the same parser downstream code will use.
- Do not treat prompt-only instructions like "return JSON" as constrained decoding.

## Boundaries

Use `sglang-openai-server` for lifecycle and `/v1` route checks. Use `sglang-tool-reasoning` when the schema belongs to tool calls or reasoning separation. Use `sglang-offline-runtime` for frontend-only constrained generation.
