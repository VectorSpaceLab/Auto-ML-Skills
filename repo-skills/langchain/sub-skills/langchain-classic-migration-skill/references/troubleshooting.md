# Classic Migration Troubleshooting

- Legacy import still works locally but fails elsewhere: install `langchain-classic` or migrate imports.
- Output changed from string to message: chat models return message objects; add `StrOutputParser` when needed.
- `.run` no longer exists: use LCEL `.invoke` with the correct input shape.
- Memory not applied: check `history_messages_key`, `input_messages_key`, and config session id.
- Provider wrapper moved: install and import the specific provider integration package.
- Callback/tracing changed: pass runtime config and LangSmith environment variables explicitly.
