---
name: sglang-tool-reasoning
description: "Configure SGLang function calling, tool-call parsers, reasoning parsers, thinking separation, and chat templates."
disable-model-invocation: true
---

# SGLang Tool And Reasoning

Use this sub-skill for OpenAI tools/functions, `--tool-call-parser`, `--reasoning-parser`, strict tool validation, thinking separation, Responses-style tools, and custom chat templates. It owns the fragile boundary between model text, tool-call JSON, and reasoning/thinking fields.

Read [references/tool-reasoning.md](references/tool-reasoning.md) for parser flags, tool schema patterns, reasoning separation, and chat-template caveats. Use [scripts/validate_tool_payload.py](scripts/validate_tool_payload.py) to lint OpenAI tool definitions before requests.

## Use When

- The user wants function/tool calling through OpenAI-compatible chat or Responses API.
- The user needs `--tool-call-parser`, `--reasoning-parser`, strict tool schemas, thinking separation, or custom chat templates.
- The user asks why tool calls are emitted as plain text or why reasoning content leaks into final answers.
- The user needs to validate tool payloads before hitting a live server.

## Inputs To Collect

- Model family, chat template, parser name, endpoint family, tool schema, strictness, desired tool-choice policy, and expected final-answer behavior.
- Whether reasoning/thinking should be returned, hidden, separated, or stripped before downstream processing.
- Server command, OpenAI client version, and sample request/response when debugging.

## Workflow

1. Determine whether the user needs OpenAI tool calling, parser-only extraction, or reasoning/thinking separation.
2. Start server with the model-appropriate `--tool-call-parser` and/or `--reasoning-parser`.
3. Validate tool JSON schema and `strict` behavior before sending traffic.
4. For chat template rendering bugs, distinguish OpenAI server chat templates from the SGLang language frontend chat templates.
5. Inspect actual response fields instead of relying only on rendered text.

## Verification

- Run the tool payload validator before the server request.
- Smoke with one tool, one required argument, deterministic generation, and a prompt that clearly requires the tool.
- A normal text completion with no tool call does not prove parser support; verify the structured tool-call field or documented fallback.

## Boundaries

Use `sglang-openai-server` for lifecycle and base `/v1` requests. Use `sglang-structured-outputs` for non-tool JSON/regex constraints. Use `sglang-install-build-troubleshooting` when parser flags are absent or rejected by the installed package.
