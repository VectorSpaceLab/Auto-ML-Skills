# Installation

Use public packages, not a private source checkout.

## Base

```bash
python -m pip install -U pip setuptools wheel
pip install -U langgraph
python -c "from langgraph.graph import StateGraph; print(StateGraph.__name__)"
```

`langgraph` bundles the core graph APIs and the `langgraph.prebuilt` helpers used for `ToolNode`, `tools_condition`, and `create_react_agent`.

## Optional Packages

- `langgraph-cli[inmem]`: local development server, `langgraph dev`, templates, Docker build helpers, and in-memory runtime extras.
- `langgraph-checkpoint-sqlite`: SQLite checkpointer for local durable persistence.
- `langgraph-checkpoint-postgres`: Postgres checkpointer for production-style durable persistence.
- LangChain provider packages such as `langchain-openai` or `langchain-anthropic`: only needed for real model-backed agents.

## No-Key Smoke Path

Use local deterministic functions for graph nodes and tools. A real chat model is not required to validate:

- `StateGraph` build/compile/invoke/stream.
- `Command` and `Send` routing.
- `InMemorySaver` checkpointing with `thread_id`.
- `interrupt()` and resume with `Command(resume=...)`.
- `ToolNode` execution with direct tool calls.
- `langgraph.json` shape for CLI projects.

Run:

```bash
python scripts/check_langgraph_env.py
python scripts/inspect_langgraph_api.py --summary
```

## Version Notes

- `MessageGraph` is deprecated in recent LangGraph versions. Prefer `StateGraph` with a `messages` key annotated by `add_messages` or `MessagesState`.
- `config_schema` on `StateGraph` is deprecated. Prefer `context_schema` for run-scoped immutable context.
- `create_react_agent` remains available in `langgraph.prebuilt`, but newer LangChain agent APIs may be preferred for generic agent factory use. Use this skill for LangGraph-specific behavior and internals.
