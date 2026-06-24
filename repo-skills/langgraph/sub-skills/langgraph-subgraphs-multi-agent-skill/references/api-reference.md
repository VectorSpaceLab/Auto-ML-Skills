# API Reference

## Compiled Subgraph As Node

A compiled graph can be added as a node to another graph when its input and output state shape fits the parent flow.

```python
child = child_builder.compile()
parent.add_node("child", child)
```

Use wrapper functions when schemas differ:

```python
def call_child(parent_state):
    child_out = child.invoke({"task": parent_state["task"]})
    return {"child_result": child_out["result"]}
```

## Parent Command

From inside a subgraph, `Command(graph=Command.PARENT, goto="parent_node", update=...)` can route to a node in the parent graph.

## Send

`Send("worker", payload)` dynamically schedules one or many worker calls. Combine it with `Annotated[..., reducer]` on output keys.

## Stream Namespaces

Use `stream(..., subgraphs=True)` or event streams with subgraph support when debugging nested execution.
