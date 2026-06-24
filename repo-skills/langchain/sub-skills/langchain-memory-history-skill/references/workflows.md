# Memory And History Workflows

## Session Store

```python
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

## Prompt With History

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Be concise."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
```

Wrap the runnable:

```python
with_history = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="question",
    history_messages_key="history",
)
```

Invoke with session config. Keep session IDs non-secret and stable.

## Persistence

For production, replace in-memory history with a persistent store. Validate serialization of message roles, content, tool calls, and metadata.
