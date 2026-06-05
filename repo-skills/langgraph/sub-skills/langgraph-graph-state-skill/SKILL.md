---
name: langgraph-graph-state-skill
description: "Use when a user wants LangGraph Graph API work with StateGraph, MessageGraph, reducers, Annotated state, nodes, edges, conditional edges, Command, Send, build, compile, invoke, or stream."
disable-model-invocation: true
---

# LangGraph Graph State

Use this sub-skill for local graph construction and routing. It covers the builder API and compiled graph runtime without requiring model provider keys.

## Short Workflow

1. Confirm imports with `../../scripts/check_langgraph_env.py`.
2. Define state with `TypedDict`, Pydantic, dataclass, or `MessagesState`.
3. Use reducers for keys written by multiple nodes: `Annotated[list[T], operator.add]`, `Annotated[list[AnyMessage], add_messages]`, or a custom two-argument reducer.
4. Add nodes before edges. Use `START` and `END` sentinels for entry and finish.
5. For conditional edges, provide `path_map` or a `Literal[...]` return type when visualization matters.
6. Compile once after all nodes and edges are added, then use `invoke`, `stream`, `ainvoke`, or `astream`.
7. Run [scripts/smoke_graph_state.py](scripts/smoke_graph_state.py) before adapting a complex graph.

## References

- [references/api-reference.md](references/api-reference.md): core imports, state schemas, reducers, graph construction, `Command`, and `Send`.
- [references/workflows.md](references/workflows.md): build patterns for sequential, conditional, message, and map-reduce graphs.
- [references/troubleshooting.md](references/troubleshooting.md): graph-specific failure modes.

## Bundled Scripts

- [scripts/smoke_graph_state.py](scripts/smoke_graph_state.py): no-key smoke test for reducers, conditional edges, `Command`, and `Send`.

## Boundaries

Use `langgraph-checkpoint-interrupt-skill` when persistence or human resume is required. Use `langgraph-prebuilt-tools-agent-skill` when the graph is primarily a tool-calling agent.
