# API Reference

## Imports

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import END, START, MessageGraph, MessagesState, StateGraph, add_messages
from langgraph.types import Command, Send
```

## StateGraph

`StateGraph(State)` creates a builder. Nodes read the current state and return a partial state update.

```python
class State(TypedDict):
    topic: str
    route: str
    notes: Annotated[list[str], list.__add__]

builder = StateGraph(State)
builder.add_node("draft", draft)
builder.add_node("review", review)
builder.add_edge(START, "draft")
builder.add_conditional_edges("draft", route, {"review": "review", "end": END})
graph = builder.compile()
```

After compile, use `graph.invoke(input)`, `graph.stream(input, stream_mode="updates")`, `graph.ainvoke(input)`, or `graph.astream(input)`.

## Reducers

Reducers merge multiple writes to the same state key. A reducer has shape `(old_value, new_value) -> merged_value`.

```python
import operator
from typing import Annotated

class State(TypedDict):
    items: Annotated[list[str], operator.add]
```

For chat-like state, prefer:

```python
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
```

`MessagesState` is a built-in `TypedDict` with a `messages` key using `add_messages`.

`MessageGraph` still exists but is deprecated in recent versions. Prefer `StateGraph` with a message reducer.

## Edges

- `add_edge(START, "node")`: entry edge.
- `add_edge("node", END)`: finish edge.
- `add_edge(["a", "b"], "join")`: wait for all listed nodes before `join`.
- `add_conditional_edges("node", router, path_map)`: route based on a callable result.

Use `path_map` to map semantic route labels to node names:

```python
def router(state: State) -> Literal["search", "answer"]:
    return "search" if state["needs_search"] else "answer"

builder.add_conditional_edges("decide", router, {"search": "search", "answer": "answer"})
```

## Command

Return `Command(update=..., goto=...)` from a node when a state update and route decision belong together.

```python
def decide(state: State) -> Command[Literal["answer", "retry"]]:
    if state["ok"]:
        return Command(update={"route": "answer"}, goto="answer")
    return Command(update={"route": "retry"}, goto="retry")
```

`Command.PARENT` routes from a subgraph to its parent graph.

## Send

Return `Send("node", arg)` from a conditional edge or inside `Command(goto=...)` for dynamic fan-out. The sent `arg` can be a different state shape expected by the target node.

```python
def fan_out(state: State):
    return [Send("worker", {"item": item}) for item in state["items"]]
```

Use a reducer on the parent state key that collects worker results.
