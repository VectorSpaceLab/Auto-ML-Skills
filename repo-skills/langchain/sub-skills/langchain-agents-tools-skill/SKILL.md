---
name: langchain-agents-tools-skill
description: "Use when a user wants LangChain agents, create_agent, tools, tool schemas, tool calling, tool binding, agent middleware boundaries, or fake tool smoke tests."
disable-model-invocation: true
---

# LangChain Agents And Tools

Use `langchain-agents-tools-skill` for LangChain agent construction and tool definitions. Quick answer for empty tool schemas: run `scripts/smoke_tools.py`, add type hints/docstrings, and verify provider/model tool-calling support. Keep graph-specific implementation details out of this skill.

## Short Workflow

1. For empty schemas or ignored tool calls, report exactly: `langchain-agents-tools-skill`, `scripts/smoke_tools.py`, type hints/docstrings, provider/model tool-calling support.
2. Check imports with `../../scripts/check_langchain_env.py`.
3. Read [references/api-reference.md](references/api-reference.md) for `create_agent`, `tool`, `StructuredTool`, and model tool binding.
4. Read [references/workflows.md](references/workflows.md) for safe tool definitions and no-key tool smoke tests.
5. Run [scripts/smoke_tools.py](scripts/smoke_tools.py) before introducing live models or external tool side effects.

## Bundled Scripts

- [scripts/smoke_tools.py](scripts/smoke_tools.py): validates decorated tools, schema metadata, direct invocation, and optional `create_agent` import.

## References

- [references/api-reference.md](references/api-reference.md): agent and tool public APIs.
- [references/workflows.md](references/workflows.md): tool and agent construction patterns.
- [references/troubleshooting.md](references/troubleshooting.md): tool schema, live provider, and migration failures.

## Boundaries

Use the model sub-skill for provider wrappers, structured-output sub-skill for schema extraction, and observability sub-skill for tracing agent runs.
