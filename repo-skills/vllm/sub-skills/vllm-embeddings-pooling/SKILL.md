---
name: vllm-embeddings-pooling
description: "Use when a user wants vLLM embeddings, pooling, classification, reranker or score workflows, offline llm.encode/llm.score usage, or OpenAI embedding-style endpoint smoke tests."
disable-model-invocation: true
---

# vLLM Embeddings And Pooling

Use this sub-skill for non-generative vLLM runners and endpoint payloads.

## Short Workflow

1. Determine whether the task is embedding, pooling, classification, reranking, or score.
2. Choose a model that supports the requested runner; generation models are not interchangeable with embedding/reranker models.
3. Read [references/workflows.md](references/workflows.md) for offline and server flow.
4. Read [references/pooling-reference.md](references/pooling-reference.md) for endpoint and payload differences.
5. Build payloads with bundled scripts, then smoke the selected endpoint with the server skill.

## Bundled Scripts

- [scripts/make_embedding_payload.py](scripts/make_embedding_payload.py): writes `/v1/embeddings` request JSON.
- [scripts/score_payload.py](scripts/score_payload.py): writes score/reranker request JSON.

## References

- [references/workflows.md](references/workflows.md): embeddings/pooling/reranking workflow.
- [references/pooling-reference.md](references/pooling-reference.md): runners, endpoints, and validation notes.

## Boundaries

Use `vllm-openai-serving` for actual server lifecycle. Use `vllm-offline-inference` for text generation.
