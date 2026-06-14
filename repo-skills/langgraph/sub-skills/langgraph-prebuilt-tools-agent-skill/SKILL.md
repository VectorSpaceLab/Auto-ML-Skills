---
name: langgraph-prebuilt-tools-agent-skill
description: "Use when a user wants LangGraph prebuilt create_react_agent, ToolNode, tools_condition, ValidationNode, tool execution, injected state, injected store, tool errors, or no-key fake agent workflows."
disable-model-invocation: true
---

# LangGraph Prebuilt Tools Agent

Use this sub-skill for `langgraph.prebuilt` components and tool-calling agent loops.

## Short Workflow

1. Confirm `langgraph.prebuilt` imports with `../../scripts/check_langgraph_env.py`.
2. For direct tool execution, use `ToolNode([tool])`.
3. For custom agent graphs, add an LLM/model node, a `ToolNode`, and route with `tools_condition`.
4. For standard ReAct-style LangGraph agents, use `create_react_agent(model, tools, ...)`.
5. Keep no-key tests deterministic with direct tool-call messages or fake chat model objects.
6. Run [scripts/smoke_prebuilt_tools.py](scripts/smoke_prebuilt_tools.py).

## References

- [references/api-reference.md](references/api-reference.md): `ToolNode`, `tools_condition`, `create_react_agent`, validation, and injected args.
- [references/workflows.md](references/workflows.md): direct tool execution, custom loop, and prebuilt agent workflow.
- [references/troubleshooting.md](references/troubleshooting.md): common tool and agent failures.

## Bundled Scripts

- [scripts/smoke_prebuilt_tools.py](scripts/smoke_prebuilt_tools.py): no-key direct `ToolNode` and `tools_condition` validation.

## Boundaries

This sub-skill does not cover LangChain's separate agent APIs. Route to the LangChain worker or skill for generic LangChain agent factory questions.
