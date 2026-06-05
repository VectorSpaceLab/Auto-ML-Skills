---
name: langchain-models-skill
description: "Use when a user wants LangChain chat models, LLMs, embeddings, provider integrations, fake models, model config, or no-key model smoke tests."
disable-model-invocation: true
---

# LangChain Models

Use this sub-skill after the root `langchain` router selects `langchain-models-skill`. It covers model wrappers, fake models, embeddings, provider package boundaries, and safe model configuration.

## Short Workflow

1. Confirm imports with `../../scripts/check_langchain_env.py`.
2. Read [references/api-reference.md](references/api-reference.md) for stable public classes and provider import patterns.
3. Read [references/configuration.md](references/configuration.md) when live provider config, timeouts, retries, streaming, or embeddings are involved.
4. Use [scripts/smoke_models.py](scripts/smoke_models.py) for a no-key model/embedding smoke test.
5. For live providers, install the matching integration package and verify that required environment variables are present without printing secrets.

## Bundled Scripts

- [scripts/smoke_models.py](scripts/smoke_models.py): runs fake chat, fake LLM, deterministic embeddings, and optional provider import checks.

## References

- [references/api-reference.md](references/api-reference.md): model, chat model, LLM, embedding, and provider imports.
- [references/configuration.md](references/configuration.md): provider configuration and live-run guardrails.
- [references/troubleshooting.md](references/troubleshooting.md): model-specific failures and migration notes.

## Boundaries

Use other sub-skills for prompts, LCEL chain assembly, retrieval, agents, structured output, streaming/event handling, or tracing.
