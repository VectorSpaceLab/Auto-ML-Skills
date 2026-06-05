# Configuration

## Package Selection

- Core graph work: `langgraph`.
- Local CLI/server work: `langgraph-cli[inmem]`.
- SQLite persistence: `langgraph-checkpoint-sqlite`.
- Postgres persistence: `langgraph-checkpoint-postgres`.
- Real model providers: provider-specific LangChain integration packages.

## Integration Checklist

- Graph module imports without side effects.
- State schemas are typed and reducers are explicit.
- Checkpointed invocations include `configurable.thread_id`.
- Tool functions have docstrings and typed arguments.
- Async nodes avoid blocking calls.
- Secrets are passed through env vars, not graph state or code.

## Migration Notes

- Prefer `StateGraph` over deprecated `MessageGraph`.
- Prefer `context_schema` over deprecated `config_schema`.
- Keep `create_react_agent` usage LangGraph-specific; generic agent factory migration may belong to LangChain APIs.
- Confirm current installed signatures before editing code generated for older LangGraph docs.
