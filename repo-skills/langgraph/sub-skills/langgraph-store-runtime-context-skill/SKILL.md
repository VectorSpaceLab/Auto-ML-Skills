---
name: langgraph-store-runtime-context-skill
description: "Use when a user wants LangGraph stores, InMemoryStore, semantic memory, runtime context, configurable values, injected store/state, cross-thread memory, or store troubleshooting."
disable-model-invocation: true
---

# LangGraph Store Runtime Context

Use `langgraph-store-runtime-context-skill` for stores and runtime context that are separate from checkpoint state. Quick answer: use `InMemoryStore` for no-key store smoke, pass a store at compile time when needed, use runtime context/configurable values for per-run settings, and validate with `scripts/smoke_store_runtime.py`.

## Short Workflow

1. Distinguish checkpoint state from store memory: checkpoints persist graph state by `thread_id`; stores hold cross-thread or semantic memory.
2. Start with `InMemoryStore` for local tests.
3. Pass store/context through compile/runtime APIs supported by the installed version.
4. Use injected store/state patterns in prebuilt tools only when tool schemas must hide internal arguments.
5. Read [references/api-reference.md](references/api-reference.md) and run [scripts/smoke_store_runtime.py](scripts/smoke_store_runtime.py).

## Bundled Scripts

- [scripts/smoke_store_runtime.py](scripts/smoke_store_runtime.py): validates `InMemoryStore` basic put/search/get behavior without model calls.
- [scripts/inspect_runtime_context.py](scripts/inspect_runtime_context.py): introspects runtime/context-related public symbols.

## References

- [references/api-reference.md](references/api-reference.md): store imports, namespace/key/value shape, and runtime context notes.
- [references/workflows.md](references/workflows.md): semantic memory, cross-thread memory, and tool injection patterns.
- [references/troubleshooting.md](references/troubleshooting.md): store vs checkpoint confusion, namespace mistakes, and version drift.

## Boundaries

Use persistence backends for checkpoint durability. Use prebuilt tools agent skill for `InjectedState` / `InjectedStore` inside `ToolNode` workflows.
