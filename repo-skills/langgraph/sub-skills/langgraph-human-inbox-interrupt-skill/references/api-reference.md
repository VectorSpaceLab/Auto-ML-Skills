# Human Inbox API Reference

## Imports

```python
from langgraph.types import Command, interrupt
```

Schema types may be available from:

```python
from langgraph.prebuilt.interrupt import HumanInterrupt, HumanResponse
```

Some schema types may move across versions. Treat them as typed helpers around normal `interrupt()` payloads.

## Request Shape

```python
request = {
    "action_request": {"action": "approve_tool", "args": {"id": "123"}},
    "config": {
        "allow_accept": True,
        "allow_ignore": True,
        "allow_respond": True,
        "allow_edit": False,
    },
    "description": "Approve this action.",
}
response = interrupt([request])[0]
```

## Resume Shape

If the interrupt value is a list, resume with a list:

```python
graph.invoke(Command(resume=[{"type": "accept"}]), config)
```

For a single scalar interrupt value, resume with a scalar.

## Required Runtime

Interrupt/resume needs a checkpointer and stable `thread_id`.
