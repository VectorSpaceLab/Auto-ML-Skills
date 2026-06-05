---
name: sglang-structured-outputs
description: "Configure SGLang JSON schema, regex, EBNF, structural tags, choices, and constrained decoding."
disable-model-invocation: true
---

# SGLang Structured Outputs

Use this sub-skill for JSON schema, regex, EBNF, structural tags, constrained decoding backends, frontend choices/select, and validation of request payloads.

Read [references/structured-outputs.md](references/structured-outputs.md). Use [scripts/validate_constraints.py](scripts/validate_constraints.py) to check mutual exclusivity and schema/regex syntax.

## Workflow

1. Pick one constraint mechanism: JSON schema for objects, regex for compact lexical formats, EBNF for grammar, structural tags for tool-style sections, or choices for classification.
2. Validate the constraint locally before sending requests.
3. Use native `/generate` or language frontend for SGLang-specific constraint fields; OpenAI-compatible routes can carry response-format/tool fields when supported by the server parser.
4. For reasoning models with hidden thinking, route combined questions to `sglang-tool-reasoning`.
