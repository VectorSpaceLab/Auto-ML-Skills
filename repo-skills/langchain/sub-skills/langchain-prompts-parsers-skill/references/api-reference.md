# Prompts And Parsers API Reference

## Prompt Classes

```python
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
```

Common constructors:

- `ChatPromptTemplate.from_messages([...])`
- `ChatPromptTemplate.from_template("... {var} ...")`
- `PromptTemplate.from_template("... {var} ...")`

Messages in chat prompts can be tuples such as `("system", "...")`, `("human", "{question}")`, and placeholders such as `MessagesPlaceholder("history")`.

## Message Classes

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
```

Use messages when a model or chain needs explicit roles or previous conversation state.

## Output Parsers

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser
```

Use `StrOutputParser` to convert model messages to strings, `JsonOutputParser` for JSON text, and `PydanticOutputParser` when validating generated JSON against a Pydantic model.
