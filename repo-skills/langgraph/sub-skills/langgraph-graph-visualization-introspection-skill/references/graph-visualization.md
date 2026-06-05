# Graph Visualization Workflow

## JSON Inspection

Use JSON when debugging:

- node ids
- edge sources/targets
- conditional flags
- subgraph expansion with `xray=True`

```python
structure = graph.get_graph().to_json()
```

## Mermaid Text

Use Mermaid text when returning diagrams to users:

```python
print(graph.get_graph().draw_mermaid())
```

This avoids PNG renderer dependencies and makes the output reviewable.

## Conditional Routing Diagrams

If a router can return multiple values but LangGraph cannot infer them, the diagram may look like the router can go everywhere. Add `path_map` or a precise return type.

## Command Destinations

When nodes return `Command(goto=...)`, add `destinations` to the node so the diagram communicates possible paths:

```python
builder.add_node("router", router, destinations=("a", "b", "__end__"))
```

## Subgraphs

Use `xray=True` for deeper inspection when subgraphs are compiled into parent graphs.
