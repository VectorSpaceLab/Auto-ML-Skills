# Graph State Troubleshooting

- Add all nodes before adding edges to them.
- Recompile after editing a builder. A compiled graph is not updated by later builder mutations.
- Use reducers for keys that receive parallel writes or repeated message appends.
- Use `path_map` with conditional edges when route labels are not exact node names.
- Avoid `MessageGraph` for new code; use `MessagesState` or `Annotated[..., add_messages]`.
- When returning `Command`, type the destination names with `Literal[...]` where possible.
- When using `Send`, the target node must accept the payload shape sent in `Send(..., arg)`.
