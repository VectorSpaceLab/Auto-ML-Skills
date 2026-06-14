# Graph Visualization API Reference

## Core Calls

```python
compiled = builder.compile()
drawable = compiled.get_graph()
data = drawable.to_json()
mermaid = drawable.draw_mermaid()
xray_data = compiled.get_graph(xray=True).to_json()
```

`to_json()` returns a node/edge structure suitable for debugging. `draw_mermaid()` returns Mermaid text.

## Conditional Edge Clarity

Use one of these:

```python
builder.add_conditional_edges("router", route, path_map={"ok": "next", "done": END})
```

or return type hints such as `Literal["next", "__end__"]` when appropriate.

## Destinations

`add_node(..., destinations=...)` helps graph rendering for nodes that return `Command` destinations. It does not itself implement routing; it documents possible visual targets.

## PNG Boundary

`draw_mermaid_png()` may need extra dependencies or online rendering depending on environment. Prefer Mermaid text for deterministic skill workflows.
