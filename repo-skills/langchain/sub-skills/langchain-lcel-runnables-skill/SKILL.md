---
name: langchain-lcel-runnables-skill
description: "Use when a user wants LangChain LCEL runnable chains, RunnableLambda, RunnableParallel, RunnablePassthrough, routing, retries, fallbacks, config, or graph inspection."
disable-model-invocation: true
---

# LangChain LCEL Runnables

Use this sub-skill for LCEL composition and runnable debugging.

## Short Workflow

1. Check `langchain_core` import status with `../../scripts/check_langchain_env.py`.
2. Read [references/api-reference.md](references/api-reference.md) for runnable classes and methods.
3. Read [references/workflows.md](references/workflows.md) for chain composition, assignment, routing, retries, and config.
4. Run [scripts/smoke_lcel.py](scripts/smoke_lcel.py) for deterministic no-key LCEL validation.

## Bundled Scripts

- [scripts/smoke_lcel.py](scripts/smoke_lcel.py): validates sequence, parallel mapping, assignment, batch, async, and fallback behavior.

## References

- [references/api-reference.md](references/api-reference.md): runnable classes, methods, and config.
- [references/workflows.md](references/workflows.md): LCEL recipes.
- [references/troubleshooting.md](references/troubleshooting.md): shape and config failures.

## Boundaries

Use model, prompt, retrieval, memory, structured output, streaming, or observability sub-skills for domain-specific details.
