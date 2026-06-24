# State Debug Time Travel Troubleshooting

- `get_state` empty: wrong `thread_id` or missing checkpointer.
- No history: saver is process-local and was restarted, or history was not persisted.
- Manual update ignored: check `as_node`, checkpoint config, and reducer behavior.
- Infinite loop: inspect conditional routing, `Command(goto=...)`, and recursion limit.
- Parallel writes conflict: add reducers for multi-writer keys.
- Debug stream too noisy: switch between `updates`, `values`, `debug`, and `tasks` modes.
