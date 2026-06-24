# Memory And History Troubleshooting

- Missing `session_id`: pass `config={"configurable": {"session_id": "..."}}`.
- Prompt variable mismatch: `history_messages_key` must match the `MessagesPlaceholder` name.
- Current input not recorded: set `input_messages_key` when chain input is a dict.
- Cross-user leakage: do not reuse a single in-memory history for all users unless intended.
- Classic memory import fails: install/use `langchain-classic` or migrate to `RunnableWithMessageHistory`.
