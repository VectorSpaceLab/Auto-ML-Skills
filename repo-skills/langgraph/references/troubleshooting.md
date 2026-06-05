# Troubleshooting

## Import Failures

- `ModuleNotFoundError: langgraph`: install `langgraph`.
- `ModuleNotFoundError: langgraph.checkpoint.sqlite`: install `langgraph-checkpoint-sqlite`.
- `ModuleNotFoundError: langgraph.checkpoint.postgres`: install `langgraph-checkpoint-postgres`.
- `langgraph` CLI command missing: install `langgraph-cli` or `langgraph-cli[inmem]`.

## Graph Build Failures

- Node name is unknown: call `add_node()` before adding edges to that node.
- `START` used as an end node or `END` used as a start node: reverse the edge.
- Conditional graph visualization shows edges to every node: add a `path_map` or a `Literal[...]` return type on the router.
- Multiple parallel writes to the same state key fail or overwrite unexpectedly: annotate that key with a reducer such as `operator.add` or `add_messages`.

## Runtime Failures

- A compiled graph ignores later builder edits: rebuild or recompile after all nodes and edges are added.
- A checkpointed graph errors about missing configurable keys: invoke with `{"configurable": {"thread_id": "stable-id"}}`.
- Interrupt resume repeats earlier node logic: this is expected. Keep side effects before `interrupt()` idempotent or move them after resume.
- ToolNode cannot find messages: pass a state containing the configured `messages_key`, a message list, or direct tool-call dictionaries.

## Persistence Failures

- Postgres checkpointer needs `.setup()` before first use.
- Manual Postgres connections should use autocommit and dict-style rows for the documented saver path.
- Use unique `thread_id` values for independent conversations or runs. Reuse a `thread_id` only when intentionally continuing state.

## Streaming Failures

- `stream_mode="messages"` requires model/token callbacks; pure deterministic nodes usually show `values`, `updates`, `debug`, or `tasks` more clearly.
- Async streams must be consumed with `async for`.
- Include `subgraphs=True` when subgraph namespaces are required.

## CLI And Platform Failures

- `langgraph dev` needs a `langgraph.json` with valid dependency entries and graph import specs.
- A graph spec should look like `./package/module.py:graph` or an importable module path plus exported graph variable.
- Hosted deployment requires service credentials and environment variables; local config validation can run without provider keys.
