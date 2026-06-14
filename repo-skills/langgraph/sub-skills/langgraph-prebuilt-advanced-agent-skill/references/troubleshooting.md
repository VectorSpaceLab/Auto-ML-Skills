# Prebuilt Advanced Agent Troubleshooting

## Structured Output Fails

Check that the model supports structured output. If the model lacks `.with_structured_output()`, use a prompt/parser workflow instead.

## Hook Does Not Change State

Return a state update dictionary from the hook. In-place mutation is not a reliable state update.

## ToolNode Direct Invoke Errors

Run `ToolNode` inside a compiled `StateGraph`; current runtime expects config/context that direct calls may not provide.

## Wrapper Breaks Tool Schema

Keep wrapper changes aligned with the tool's Pydantic/input schema. Validate with a fake tool call before using a model.

## Tool Error Leaks Secrets

Sanitize `handle_tool_errors` messages before they are returned to the model.
