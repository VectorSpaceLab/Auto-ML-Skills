# Workflows

## Sequential Graph

1. Define `State`.
2. Add one node per transformation.
3. Add `START -> first`, intermediate edges, and final `node -> END`.
4. Compile and invoke.

## Conditional Graph

1. Write a router that returns a route label or node name.
2. Prefer a `Literal[...]` return annotation or a `path_map`.
3. Use `END` in the `path_map` for termination.

## Message Graph

Prefer `StateGraph`:

```python
class State(MessagesState):
    topic: str
```

Nodes can return:

```python
{"messages": [{"role": "assistant", "content": "hello"}]}
```

`add_messages` merges by message ID, appends new messages, and supports message removal semantics from LangChain message objects.

## Map-Reduce Fan-Out

1. Parent state has an input list and an output list with a reducer.
2. A conditional edge from `START` or a planner node returns a list of `Send` packets.
3. Worker nodes receive the per-item payload.
4. Worker outputs write to the reducer key.

## Command Routing

Use `Command` when a node both updates state and chooses the next node. This reduces split-brain bugs where a router reads stale state written by the previous node.
