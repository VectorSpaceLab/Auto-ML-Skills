---
name: sglang-tool-reasoning
description: "Configure SGLang function calling, tool-call parsers, reasoning parsers, thinking separation, and chat templates."
disable-model-invocation: true
---

# SGLang Tool And Reasoning

Use this sub-skill for OpenAI tools/functions, `--tool-call-parser`, `--reasoning-parser`, strict tool validation, thinking separation, and custom chat templates.

Read [references/tool-reasoning.md](references/tool-reasoning.md). Use [scripts/validate_tool_payload.py](scripts/validate_tool_payload.py) to lint OpenAI tool definitions before requests.

## Workflow

1. Determine whether the user needs OpenAI tool calling, parser-only extraction, or reasoning/thinking separation.
2. Start server with the model-appropriate `--tool-call-parser` and/or `--reasoning-parser`.
3. Validate tool JSON schema and `strict` behavior before sending traffic.
4. For chat template rendering bugs, distinguish OpenAI server chat templates from the SGLang language frontend chat templates.
