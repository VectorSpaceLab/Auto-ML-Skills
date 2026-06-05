# Pooling Reference

## Runner Families

- Embedding: maps text to vectors.
- Pooling: model-specific pooled hidden states.
- Classification: labels or class scores.
- Reward: reward-model style scalar or token-level output, depending on model.
- Score/rerank: relevance score for text pairs.

Offline APIs:

- `LLM.embed(...)` for embedding models where exposed.
- `LLM.encode(..., pooling_task=...)` for pooling-family tasks.
- `LLM.classify(...)` for classification models.
- `LLM.score(...)` for score/reranker models.

Generation models are not interchangeable with pooling models unless the endpoint explicitly supports a generative scoring workflow.

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

Classification candidate:

```json
{
  "model": "jason9693/Qwen2.5-1.5B-apeach",
  "input": ["vLLM is useful for serving."]
}
```

Generative scoring candidate for a CausalLM:

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "query": "Is this city the capital of France?",
  "documents": ["Paris", "London"],
  "label_token_ids": [9454, 2753]
}
```

Score, rerank, classify, and pooling schemas vary by version; inspect request classes before relying on field names.

## Endpoint Selection

- Use `/v1/embeddings` or `/v2/embed` for embedding models.
- Use `/score` or `/v1/score` for score models.
- Use `/rerank`, `/v1/rerank`, or `/v2/rerank` for reranker-style APIs.
- Use `/classify` for classification models.
- Use `/pooling` for generic pooling output.
- Use `/generative_scoring` only for CausalLM next-token label scoring.
