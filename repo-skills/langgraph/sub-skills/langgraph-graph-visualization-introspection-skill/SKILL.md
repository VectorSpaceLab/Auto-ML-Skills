---
name: langgraph-graph-visualization-introspection-skill
description: "Use when a user wants LangGraph get_graph, xray graph introspection, Mermaid diagrams, to_json, draw_mermaid, conditional edge visualization, path_map, destinations, or diagram troubleshooting."
disable-model-invocation: true
---

# LangGraph Graph Visualization Introspection

Use `langgraph-graph-visualization-introspection-skill` to inspect compiled graph structure or produce diagrams. Quick answer: call `compiled.get_graph()`, use `.to_json()` for machine-readable structure, `.draw_mermaid()` for text diagrams, and add `path_map`, `Literal` return types, or `destinations` to keep conditional-edge diagrams readable.

## Short Workflow

1. Compile the graph.
2. Call `graph.get_graph()` or `graph.get_graph(xray=True)`.
3. Use `to_json()` for debugging nodes/edges.
4. Use `draw_mermaid()` for a text diagram; avoid PNG rendering unless dependencies/network are available.
5. For conditional routing, provide `path_map` or typed literal destinations so diagrams do not show spurious edges.
6. Run [scripts/smoke_graph_visualization.py](scripts/smoke_graph_visualization.py).

## Bundled Scripts

- [scripts/smoke_graph_visualization.py](scripts/smoke_graph_visualization.py): builds a small graph, emits JSON and Mermaid, and checks conditional edge metadata.

## References

- [references/graph-visualization.md](references/graph-visualization.md): diagram and introspection workflow.
- [references/api-reference.md](references/api-reference.md): relevant graph introspection calls.
- [references/troubleshooting.md](references/troubleshooting.md): noisy conditional edges, PNG failures, and xray confusion.

## Boundaries

Use graph-state skill for graph construction and state semantics. Use this skill when visualization, diagram quality, or structural debugging is the main task.
