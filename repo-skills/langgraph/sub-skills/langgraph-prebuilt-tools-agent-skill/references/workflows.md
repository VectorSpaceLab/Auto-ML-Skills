# Workflows

## Direct Tool Smoke

1. Define small typed Python functions.
2. Create `ToolNode([fn])`.
3. Prefer placing the `ToolNode` in a compiled `StateGraph`.
4. Assert a `ToolMessage` is returned.

## Custom Agent Loop

1. State contains `messages` with `add_messages`.
2. Model node appends an AI message.
3. Tool node executes tool calls.
4. `tools_condition` routes from model to tools or `END`.
5. `tools -> model` edge loops until no tool calls remain.

## Prebuilt ReAct Agent

1. Install the needed model provider package.
2. Define tools with docstrings and typed args.
3. Create `app = create_react_agent(model, tools, checkpointer=optional_checkpointer)`.
4. Invoke with `{"messages": [{"role": "user", "content": "..."}]}`.
5. If checkpointed, pass `configurable.thread_id`.

## Validation Node

Use `ValidationNode` when the model emits structured tool calls that should be validated before execution. Route invalid calls back to the model or an error handling node.
