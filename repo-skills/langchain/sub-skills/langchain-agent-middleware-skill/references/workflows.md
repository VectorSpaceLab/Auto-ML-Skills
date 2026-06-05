# Agent Middleware Workflows

## Dynamic Prompt Or Context

1. Identify runtime context needed by the agent.
2. Inject only non-secret, task-relevant fields.
3. Keep prompt construction deterministic and testable.
4. Trace metadata separately from prompt content.

## Guardrail Or Validation

1. Decide whether validation happens before model, after model, or around tool calls.
2. Fail closed for unsafe tool calls.
3. Return clear errors to the agent loop.
4. Keep side effects idempotent.

## Tool Call Control

Middleware can approve, reject, rewrite, or annotate tool calls, but the underlying tools still need good schemas from `langchain-agents-tools-skill`.
