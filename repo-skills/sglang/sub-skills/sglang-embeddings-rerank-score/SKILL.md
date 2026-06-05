---
name: sglang-embeddings-rerank-score
description: "Use SGLang embedding, classify, rerank, score, and reward-model endpoints and payloads."
disable-model-invocation: true
---

# SGLang Embeddings, Rerank, Score

Use this sub-skill for `/v1/embeddings`, `/v1/rerank`, `/v1/score`, `/v1/classify`, native `/encode`, native `/classify`, and reward model score extraction.

Read [references/embeddings-rerank-score.md](references/embeddings-rerank-score.md). Use [scripts/validate_retrieval_payload.py](scripts/validate_retrieval_payload.py) to lint endpoint payloads.

## Workflow

1. Confirm endpoint and model type: embedding, reranker, classifier, reward model, or score/logprob.
2. Launch embedding servers with `--is-embedding` when required by the model/endpoint.
3. Use OpenAI `/v1/embeddings` for client compatibility; native `/encode` for SGLang-specific features.
4. Check output shape and normalization expectations in downstream code.
