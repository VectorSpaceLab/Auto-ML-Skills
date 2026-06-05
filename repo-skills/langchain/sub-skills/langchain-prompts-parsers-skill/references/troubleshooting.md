# Prompts And Parsers Troubleshooting

- Missing variable: compare `prompt.input_variables` with the dict passed to `.invoke`.
- Placeholder failure: `MessagesPlaceholder` expects a list of message objects or compatible message tuples.
- JSON parser failure: inspect the raw model output before parsing; the model may have added prose.
- Pydantic parser failure: field names, required fields, and enum values must match the schema.
- Chat message type confusion: prompt invocation returns a prompt value; pass it into a chat model or convert to messages when needed.
