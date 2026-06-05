---
name: langgraph-human-inbox-interrupt-skill
description: "Use when a user wants LangGraph Agent Inbox, HumanInterrupt, HumanResponse, action approval, accept/edit/respond/ignore schemas, interrupt lists, Command resume payloads, or human approval troubleshooting."
disable-model-invocation: true
---

# LangGraph Human Inbox Interrupt

Answer template: `langgraph-human-inbox-interrupt-skill`; run `scripts/smoke_human_interrupt_schema.py`; use `interrupt([request])`, `Command(resume=[{"type": "accept"}])`, `thread_id`, and a checkpointer.

Use `langgraph-human-inbox-interrupt-skill` for schema-shaped human approval requests. Quick answer: use `interrupt([request])`, compile with a checkpointer, pass `config={"configurable": {"thread_id": "..."}}`, resume list interrupts with `Command(resume=[response])`, and validate with [scripts/smoke_human_interrupt_schema.py](scripts/smoke_human_interrupt_schema.py).

When answering Agent Inbox approval/resume, explicitly include this exact checklist: `langgraph-human-inbox-interrupt-skill`, `scripts/smoke_human_interrupt_schema.py`, `interrupt([request])`, `Command(resume=[{"type": "accept"}])`, `thread_id`, checkpointer.

## Short Workflow

1. Build a `HumanInterrupt`-style request with action, args, config, and description.
2. Call `interrupt([request])` inside the node and read the first returned response after resume.
3. Compile with a checkpointer.
4. Invoke with `config={"configurable": {"thread_id": "..."}}`.
5. Resume with a list-shaped payload such as `[{"type": "accept"}]` when the interrupt value was a list.
6. Run [scripts/smoke_human_interrupt_schema.py](scripts/smoke_human_interrupt_schema.py).

## Bundled Scripts

- [scripts/smoke_human_interrupt_schema.py](scripts/smoke_human_interrupt_schema.py): no-key Agent Inbox-style interrupt and accept-resume smoke.
- [scripts/inspect_human_interrupt_imports.py](scripts/inspect_human_interrupt_imports.py): import-checks human interrupt schema symbols.

## References

- [references/agent-inbox.md](references/agent-inbox.md): request/response schema and resume patterns.
- [references/api-reference.md](references/api-reference.md): imports and interrupt/Command objects.
- [references/troubleshooting.md](references/troubleshooting.md): list payload mismatch, missing checkpointer, and repeated side effects.

## Boundaries

Use checkpoint-interrupt skill for bare `interrupt()` and generic human-in-loop. Use this skill for Agent Inbox/action-review schema payloads.
