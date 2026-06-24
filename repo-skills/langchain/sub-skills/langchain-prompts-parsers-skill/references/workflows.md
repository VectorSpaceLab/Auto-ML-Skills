# Prompt And Parser Workflows

## Format A Chat Prompt

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer in {style}."),
    ("human", "{question}"),
])
messages = prompt.invoke({"style": "one sentence", "question": "What is LCEL?"})
```

## Prompt To Model To String

```python
chain = prompt | model | StrOutputParser()
text = chain.invoke({"style": "one sentence", "question": "What is LCEL?"})
```

## Conversation Placeholder

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Be concise."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
```

The caller must provide `history` as a list of message objects unless the placeholder is optional.

## JSON Parsing

Use `JsonOutputParser` when the model output is JSON text. For Pydantic validation, use `PydanticOutputParser` or the structured-output sub-skill if the model supports native structured output.
