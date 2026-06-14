---
name: langchain-structured-output-skill
description: "Use when a user wants LangChain structured output, Pydantic schemas, JSON schema, with_structured_output, JSON parsers, tool/function parsers, or schema validation."
disable-model-invocation: true
---

# LangChain Structured Output

Use this sub-skill for schemas, structured model responses, and parser-based JSON validation.

## Short Workflow

1. Confirm imports with `../../scripts/check_langchain_env.py`.
2. Read [references/api-reference.md](references/api-reference.md) for structured-output and parser APIs.
3. Read [references/workflows.md](references/workflows.md) to choose native `with_structured_output` versus parser-based extraction.
4. Run [scripts/smoke_structured_output.py](scripts/smoke_structured_output.py) for no-key schema validation.

## Bundled Scripts

- [scripts/smoke_structured_output.py](scripts/smoke_structured_output.py): validates Pydantic and JSON parser flows.

## References

- [references/api-reference.md](references/api-reference.md): Pydantic, JSON, and tool parser APIs.
- [references/workflows.md](references/workflows.md): structured-output decision tree.
- [references/troubleshooting.md](references/troubleshooting.md): schema and provider failures.

## Boundaries

Use the models sub-skill for provider support and the prompts/parsers sub-skill for plain parser formatting.
