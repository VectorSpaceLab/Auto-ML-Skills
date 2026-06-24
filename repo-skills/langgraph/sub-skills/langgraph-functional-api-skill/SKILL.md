---
name: langgraph-functional-api-skill
description: "Use when a user wants LangGraph functional API, @task, @entrypoint, Pregel-style functions, functional workflows, checkpointed functions, or functional API troubleshooting."
disable-model-invocation: true
---

# LangGraph Functional API

Use `langgraph-functional-api-skill` when the user prefers function/task workflows instead of manually building `StateGraph`. Quick answer: inspect `langgraph.func`, use `@task` and `@entrypoint` when available, keep state/checkpoint semantics explicit, and validate symbols with `scripts/inspect_functional_api.py`.

## Short Workflow

1. Confirm installed functional API symbols with [scripts/inspect_functional_api.py](scripts/inspect_functional_api.py).
2. Use functional API for compact task graphs and StateGraph when explicit nodes/edges are clearer.
3. Keep persistence and config behavior explicit; do not hide `thread_id` requirements.
4. For complex routing, fan-out, subgraphs, or visualization, prefer StateGraph unless functional API is already established.
5. Read [references/api-reference.md](references/api-reference.md) and [references/workflows.md](references/workflows.md).

## Bundled Scripts

- [scripts/inspect_functional_api.py](scripts/inspect_functional_api.py): lists importable `langgraph.func` symbols and signatures.

## References

- [references/api-reference.md](references/api-reference.md): functional API import surface and version-sensitive signatures.
- [references/workflows.md](references/workflows.md): when to use functional API vs StateGraph.
- [references/troubleshooting.md](references/troubleshooting.md): missing decorators, hidden state, and persistence confusion.

## Boundaries

Use graph-state skill for explicit builder graphs and persistence/checkpoint skills for durable state details.
