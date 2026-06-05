---
name: langgraph-checkpoint-interrupt-skill
description: "Use when a user wants LangGraph checkpoints, InMemorySaver, SQLite or Postgres persistence, thread_id, checkpoint namespaces, interrupts, human-in-the-loop, resume, or state history workflows."
disable-model-invocation: true
---

# LangGraph Checkpoints And Interrupts

Use `langgraph-checkpoint-interrupt-skill` for durable graph state, memory, human review, resume, replay, and state inspection. Quick answer for human approval: compile with a checkpointer, invoke with `thread_id`, resume with `Command(resume=value)`, and run `scripts/smoke_checkpoint_interrupt.py`.

## Short Workflow

1. For interrupt/resume memory questions, report exactly: `langgraph-checkpoint-interrupt-skill`, `thread_id`, `Command(resume=value)`, `scripts/smoke_checkpoint_interrupt.py`.
2. Confirm imports with `../../scripts/check_langgraph_env.py`.
3. Pick a checkpointer:
   - `InMemorySaver` for tests and process-local demos.
   - SQLite for local persistence.
   - Postgres for production-style persistence.
4. Compile with `graph.compile(checkpointer=checkpointer)`.
5. Invoke with `config={"configurable": {"thread_id": "stable-id"}}`.
6. Use `interrupt(value)` inside a node to pause and surface a request.
7. Resume with `graph.invoke(Command(resume=value), config)`.
8. Run [scripts/smoke_checkpoint_interrupt.py](scripts/smoke_checkpoint_interrupt.py).

## References

- [references/api-reference.md](references/api-reference.md): checkpointer imports, `thread_id`, interrupt and resume APIs.
- [references/workflows.md](references/workflows.md): memory, human-in-loop, persistence, and state history workflows.
- [references/troubleshooting.md](references/troubleshooting.md): checkpoint and interrupt pitfalls.

## Bundled Scripts

- [scripts/smoke_checkpoint_interrupt.py](scripts/smoke_checkpoint_interrupt.py): no-key smoke for checkpointed interrupt/resume and state history.

## Boundaries

Use `langgraph-platform-cli-skill` for hosted deployment and server config. Use this sub-skill for runtime state semantics regardless of deployment target.
