# Prebuilt Tools Troubleshooting

- Missing tool docstring or type hints can produce weak schemas. Add clear docstrings and annotations.
- `tools_condition` raises when no messages are found. Ensure the state key matches `messages_key`.
- Direct tool-call dictionaries should include name, args, id, and type when bypassing message parsing.
- Tool errors are controlled by `handle_tool_errors`; use explicit handling for expected user input errors.
- Real model agents need a chat model that supports tool calling. Bind tools only when the selected model API expects it.
- Do not put secrets in tool schemas, prompts, graph state dumps, or interrupt payloads.
- If direct `ToolNode.invoke(...)` reports a missing config key for `tools`, invoke the `ToolNode` inside a compiled graph. That matches the normal LangGraph runtime path and supplies the runnable context expected by recent versions.
