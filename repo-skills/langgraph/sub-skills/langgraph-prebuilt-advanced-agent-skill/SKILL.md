---
name: langgraph-prebuilt-advanced-agent-skill
description: "Use when a user wants LangGraph create_react_agent advanced options, response_format, pre_model_hook, post_model_hook, remaining_steps, ToolNode wrap_tool_call, ToolRuntime, injected state/store, or advanced prebuilt agent troubleshooting."
disable-model-invocation: true
---

# LangGraph Prebuilt Advanced Agent

Use `langgraph-prebuilt-advanced-agent-skill` after the basic prebuilt tools/agent flow works. Quick answer: inspect `create_react_agent` advanced signature, use `response_format` only with models that support structured output, use pre/post hooks to return valid state updates, and validate tool-call wrapping with [scripts/smoke_toolnode_wrap_tool_call.py](scripts/smoke_toolnode_wrap_tool_call.py).

## Short Workflow

1. Start from `langgraph-prebuilt-tools-agent-skill` for basic `ToolNode` and `create_react_agent`.
2. Use this skill for advanced customization:
   - `response_format`
   - `pre_model_hook`
   - `post_model_hook`
   - `state_schema` / `context_schema`
   - `remaining_steps`
   - `ToolNode(wrap_tool_call=...)`
3. Confirm the model supports required structured-output/tool-call methods before enabling agent-level structured responses.
4. Validate tool wrapper behavior in a compiled graph.
5. Run [scripts/inspect_react_agent_advanced.py](scripts/inspect_react_agent_advanced.py) and [scripts/smoke_toolnode_wrap_tool_call.py](scripts/smoke_toolnode_wrap_tool_call.py).

## Bundled Scripts

- [scripts/inspect_react_agent_advanced.py](scripts/inspect_react_agent_advanced.py): prints public signatures for `create_react_agent`, `ToolNode`, `InjectedState`, and `InjectedStore`.
- [scripts/smoke_toolnode_wrap_tool_call.py](scripts/smoke_toolnode_wrap_tool_call.py): no-key compiled-graph smoke for `ToolNode(wrap_tool_call=...)`.

## References

- [references/react-agent-advanced.md](references/react-agent-advanced.md): advanced `create_react_agent` options and model capability boundaries.
- [references/toolnode-interceptors.md](references/toolnode-interceptors.md): `wrap_tool_call`, errors, and injected runtime patterns.
- [references/troubleshooting.md](references/troubleshooting.md): structured output failures, hook state updates, and ToolNode runtime config issues.

## Boundaries

Use the basic prebuilt tools/agent skill for normal ReAct agents and tool nodes. Use this skill only for advanced customization or interceptors.
