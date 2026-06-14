# Memory And History API Reference

## Chat History

```python
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
```

`InMemoryChatMessageHistory` supports adding and reading messages for local smoke tests.

## Runnable History

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
```

Key parameters:

- `runnable`: wrapped runnable or chain.
- `get_session_history`: callable that returns a chat history for a session id.
- `input_messages_key`: input key containing the current user message when inputs are dicts.
- `history_messages_key`: prompt key used by `MessagesPlaceholder`.

Runtime config usually includes:

```python
config={"configurable": {"session_id": "user-1"}}
```

## Classic Memory

Classic memory classes live in `langchain_classic.memory`. Prefer modern runnable history unless maintaining old chains.
