---
name: langchain-memory-history-skill
description: "Use when a user wants LangChain memory, chat history, conversation state, RunnableWithMessageHistory, session history, or migration from classic memory."
disable-model-invocation: true
---

# LangChain Memory And History

Use this sub-skill for conversation state and message history. Prefer runnable history wrappers for modern LCEL workflows.

## Short Workflow

1. Check imports with `../../scripts/check_langchain_env.py`.
2. Read [references/api-reference.md](references/api-reference.md) for chat history and `RunnableWithMessageHistory`.
3. Read [references/workflows.md](references/workflows.md) for session-scoped history patterns.
4. Run [scripts/smoke_memory.py](scripts/smoke_memory.py) for no-key history validation.

## Bundled Scripts

- [scripts/smoke_memory.py](scripts/smoke_memory.py): validates in-memory chat history and runnable history message injection.

## References

- [references/api-reference.md](references/api-reference.md): message history classes and wrapper parameters.
- [references/workflows.md](references/workflows.md): state handling and migration patterns.
- [references/troubleshooting.md](references/troubleshooting.md): key and schema failures.

## Boundaries

Use observability/config for tracing stateful runs and agents/tools for tool-driven agent state.
