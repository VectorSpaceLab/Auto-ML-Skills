# Agent Inbox

## Response Types

Common human response types:

- `accept`: approve the proposed action
- `ignore`: skip the action
- `response`: provide free-form human input
- `edit`: return modified action args

Design node code to handle only the response types enabled in the request config.

## Node Pattern

```python
def approval_node(state):
    request = {
        "action_request": {"action": "send_email", "args": state["draft"]},
        "config": {"allow_accept": True, "allow_edit": True, "allow_ignore": True},
        "description": "Review the draft email before sending.",
    }
    response = interrupt([request])[0]
    if response["type"] == "accept":
        return {"approved": True}
    if response["type"] == "edit":
        return {"draft": response["args"], "approved": True}
    return {"approved": False}
```

## Side Effects

Nodes re-enter after resume. Put external side effects after the interrupt response and make them idempotent.

## UI Boundary

Agent Inbox schemas are useful for UI rendering, but LangGraph itself resumes with ordinary payloads through `Command(resume=...)`.
