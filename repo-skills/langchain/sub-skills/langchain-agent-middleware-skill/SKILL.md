---
name: langchain-agent-middleware-skill
description: "Use when a user wants LangChain agent middleware, before/after model hooks, dynamic prompts, tool call control, guardrails, human approval boundaries, or middleware import checks."
disable-model-invocation: true
---

# LangChain Agent Middleware

Use `langchain-agent-middleware-skill` for LangChain 1.x agent customization around `create_agent`. Quick answer: inspect `langchain.agents.middleware`, decide whether the behavior belongs before model, after model, around tool calls, or in prompt/context, then validate imports with `scripts/inspect_agent_middleware.py`.

## Short Workflow

1. Confirm `langchain.agents.middleware` imports.
2. Decide the middleware boundary: prompt shaping, model request/response, tool call handling, guardrail, or human approval.
3. Keep tool schemas and provider tool-calling in `langchain-agents-tools-skill`; use this skill for cross-cutting agent behavior.
4. Avoid secrets in middleware state, prompts, tags, or metadata.
5. Read [references/api-reference.md](references/api-reference.md) and [references/workflows.md](references/workflows.md), then run [scripts/inspect_agent_middleware.py](scripts/inspect_agent_middleware.py).

## Bundled Scripts

- [scripts/inspect_agent_middleware.py](scripts/inspect_agent_middleware.py): lists importable middleware symbols in the installed LangChain package.

## References

- [references/api-reference.md](references/api-reference.md): middleware module, common symbol categories, and inspection guidance.
- [references/workflows.md](references/workflows.md): dynamic prompts, guardrails, approval, and tool-control patterns.
- [references/troubleshooting.md](references/troubleshooting.md): version drift and misplaced middleware behavior.

## Boundaries

Use LangGraph for durable multi-step agent control, interrupts, and checkpoints. Use LangChain middleware for LangChain agent customization within the installed agent API.
