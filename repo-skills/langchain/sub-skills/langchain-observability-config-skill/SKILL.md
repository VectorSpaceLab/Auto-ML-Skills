---
name: langchain-observability-config-skill
description: "Use when a user wants LangChain callbacks, tracing, LangSmith, tags, metadata, runnable config, runtime configuration, integration setup, or common pitfalls."
disable-model-invocation: true
---

# LangChain Observability And Config

Use this sub-skill for callbacks, tracing, LangSmith setup, runnable config, tags, metadata, and integration pitfalls.

## Short Workflow

1. Check package imports with `../../scripts/check_langchain_env.py --module langsmith`.
2. Read [references/api-reference.md](references/api-reference.md) for callbacks and config APIs.
3. Read [references/configuration.md](references/configuration.md) before enabling LangSmith or live tracing.
4. Run [scripts/smoke_observability.py](scripts/smoke_observability.py) for no-key config and callback validation.

## Bundled Scripts

- [scripts/smoke_observability.py](scripts/smoke_observability.py): validates runnable config and a local callback without external tracing.

## References

- [references/api-reference.md](references/api-reference.md): callbacks, tracers, and runnable config.
- [references/configuration.md](references/configuration.md): LangSmith and integration configuration.
- [references/troubleshooting.md](references/troubleshooting.md): tracing, callback, and metadata failures.

## Boundaries

Use other sub-skills for chain logic; return here when the question is about visibility, runtime config, or production diagnostics.
