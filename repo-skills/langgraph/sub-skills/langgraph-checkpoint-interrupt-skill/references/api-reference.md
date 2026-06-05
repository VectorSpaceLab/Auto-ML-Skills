# API Reference

## Core Imports

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt
```

Optional persistence packages:

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
```

## Compile With Checkpointer

```python
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "conversation-1"}}
graph.invoke({"messages": []}, config)
```

The `thread_id` identifies a durable run. Reuse it to continue memory; change it for an independent run.

`checkpoint_ns` can separate checkpoint namespaces for nested or advanced workflows.

## Interrupt And Resume

```python
def ask_human(state):
    answer = interrupt({"question": "Approve?"})
    return {"approved": answer}

first = graph.invoke({"approved": None}, config)
second = graph.invoke(Command(resume=True), config)
```

The node that called `interrupt()` is re-entered from the beginning on resume. Keep side effects before the interrupt idempotent.

## State Inspection

Common compiled graph methods include:

- `get_state(config)`: current checkpointed state snapshot.
- `get_state_history(config)`: checkpoint history for a thread.
- `update_state(config, values, as_node=...)`: manual state correction for human-in-loop and time travel workflows.
