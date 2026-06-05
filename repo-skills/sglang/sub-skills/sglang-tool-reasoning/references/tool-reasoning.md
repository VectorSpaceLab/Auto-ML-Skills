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
