# Pooling Reference

## Runner Families

- Embedding: maps text to vectors.
- Pooling: model-specific pooled hidden states.
- Classification: labels or class scores.
- Score/rerank: relevance score for text pairs.

## Endpoint Payloads

Embeddings:

```json
{
  "model": "BAAI/bge-small-en-v1.5",
  "input": ["first sentence", "second sentence"]
}
```

Score/rerank candidate:

```json
{
  "model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
  "text_1": "query",
  "text_2": "document"
}
```

Score schemas vary by version; inspect request classes before relying on field names.
