---
name: langgraph-subgraphs-multi-agent-skill
description: "Use when a user wants LangGraph subgraphs, nested graphs, multi-agent routing, handoffs, parent graph commands, supervisor patterns, map-reduce Send fan-out, or hierarchical agent teams."
disable-model-invocation: true
---

# LangGraph Subgraphs Multi Agent

Use this sub-skill for composing graphs into larger systems, including multi-agent and hierarchical workflows.

## Short Workflow

1. Decide whether agents share state or communicate through explicit handoff payloads.
2. Build each subgraph as a normal `StateGraph`, then compile it.
3. Add a compiled subgraph as a node in the parent graph when state schemas are compatible or adapt through wrapper nodes.
4. Use `Command(goto=...)` for handoff routing and `Command(graph=Command.PARENT, goto=...)` from subgraphs when returning control to a parent node.
5. Use `Send` for dynamic fan-out or map-reduce patterns.
6. Add reducers on parent state keys that collect child outputs.
7. Run [scripts/smoke_subgraph_multiagent.py](scripts/smoke_subgraph_multiagent.py).

## References

- [references/api-reference.md](references/api-reference.md): compiled subgraph nodes, `Command.PARENT`, `Send`, and reducers.
- [references/workflows.md](references/workflows.md): supervisor, handoff, hierarchical, and map-reduce patterns.
- [references/troubleshooting.md](references/troubleshooting.md): state schema and routing pitfalls.

## Bundled Scripts

- [scripts/smoke_subgraph_multiagent.py](scripts/smoke_subgraph_multiagent.py): no-key subgraph plus fan-out smoke.

## Boundaries

Use `langgraph-prebuilt-tools-agent-skill` when each agent is a tool-calling ReAct loop. Use this sub-skill for graph composition and handoff mechanics.
