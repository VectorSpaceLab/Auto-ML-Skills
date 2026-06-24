---
name: langchain-prompts-parsers-skill
description: "Use when a user wants LangChain prompt templates, chat messages, message placeholders, few-shot prompts, prompt formatting, or output parsers."
disable-model-invocation: true
---

# LangChain Prompts And Parsers

Use this sub-skill for prompt formatting, message construction, parser selection, and parser smoke tests.

## Short Workflow

1. Confirm `langchain_core` imports with `../../scripts/check_langchain_env.py`.
2. Read [references/api-reference.md](references/api-reference.md) for public prompt, message, and parser classes.
3. Read [references/workflows.md](references/workflows.md) for prompt-to-model-to-parser LCEL patterns.
4. Run [scripts/smoke_prompts_parsers.py](scripts/smoke_prompts_parsers.py) to validate formatting and parser behavior without keys.

## Bundled Scripts

- [scripts/smoke_prompts_parsers.py](scripts/smoke_prompts_parsers.py): checks prompt variables, messages, string parsing, JSON parsing, and Pydantic parsing.

## References

- [references/api-reference.md](references/api-reference.md): prompts, messages, placeholders, and parsers.
- [references/workflows.md](references/workflows.md): common formatting and LCEL parser flows.
- [references/troubleshooting.md](references/troubleshooting.md): prompt variable and parser failures.

## Boundaries

Use LCEL, model, structured-output, retrieval, or memory sub-skills when the task goes beyond formatting/parsing.
