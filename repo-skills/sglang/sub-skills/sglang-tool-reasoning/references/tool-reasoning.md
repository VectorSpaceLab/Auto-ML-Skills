# Tool And Reasoning Reference

## Server Flags And Env

Relevant server/router args include:

- `--tool-call-parser <parser>` for model-specific tool call parsing.
- `--reasoning-parser <parser>` for separating reasoning from final answer.
- `--chat-template` and `--hf-chat-template-name` for OpenAI-compatible server chat rendering.
- `--strip-thinking-cache` and `--enable-strict-thinking` for thinking-related behavior.
- `--tool-server` for tool-server integration.

Relevant env:

- `SGLANG_TOOL_STRICT_LEVEL=0`: no strict validation.
- `SGLANG_TOOL_STRICT_LEVEL=1`: structural tag constraints for all tools.
- `SGLANG_TOOL_STRICT_LEVEL=2`: strict parameter validation for all tools.
- `SGLANG_FORWARD_UNKNOWN_TOOLS`: forward unknown tool calls instead of dropping them.

Parser availability is build-dependent; inspect with the installed package or server help in the target environment.

## OpenAI Tool Payload

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}]
```

Send through `/v1/chat/completions` with `tools=tools` and optionally `tool_choice`.

## Responses API And Built-In Tools

For models that document OpenAI Responses API support, use `client.responses.create(...)` through `/v1/responses`. Responses requests use `instructions` and `input` rather than chat `messages`, and can carry built-in tool declarations such as code-interpreter or web-search style tools when the server has a compatible `--tool-server`.

Keep these distinctions clear:

- Chat tools: `POST /v1/chat/completions`, `messages`, `tools`, `tool_choice`.
- Responses tools: `POST /v1/responses`, `instructions`, `input`, `tools`, response retrieve/cancel routes.
- Native parser helpers: `/parse_function_call` and `/separate_reasoning`.

Do not enable a demo tool server in production without sandbox, network, and credential review. Built-in Python/code tools may execute generated code; web-search tools need explicit API credentials.

## Parser Utility Routes

Inspected native helper routes include:

- `/parse_function_call`: parse function-call output.
- `/separate_reasoning`: separate reasoning from final text.

These are useful for debugging parsers without a full OpenAI client stack, but still depend on server parser configuration.

## Chat Template Distinction

There are two chat template systems:

- OpenAI-compatible server templates, configured with server args and implemented in the server parser/conversation layer.
- SGLang language frontend templates used by frontend `sgl.system/user/assistant` and runtime backends.

Do not mix fixes for one layer into the other. If an OpenAI request renders poorly, inspect server chat template and parser flags first.
