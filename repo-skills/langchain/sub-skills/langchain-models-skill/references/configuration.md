# Model Configuration

## Live Provider Checklist

- Install the provider package, not only `langchain`.
- Collect model name, endpoint/base URL, temperature, max tokens, timeout, max retries, and streaming requirement.
- Confirm the key environment variable exists without printing its value.
- Use fake models for unit tests and CI paths that should not call external APIs.

## Chat Model Patterns

```python
model = ChatOpenAI(model="gpt-4.1-mini", temperature=0, timeout=30, max_retries=2)
result = model.invoke("Say one sentence.")
```

Streaming:

```python
for chunk in model.stream("Say three words."):
    ...
```

Async:

```python
result = await model.ainvoke("Say one sentence.")
```

## Embedding Patterns

Use provider embeddings for production indexes and deterministic fake embeddings for smoke tests:

```python
embedding = DeterministicFakeEmbedding(size=16)
vector = embedding.embed_query("hello")
```

Keep embedding dimensions consistent with the vector store index.
