---
name: vllm-embeddings-pooling
description: "Use when a user wants vLLM embeddings, pooling, classification, reranker or score workflows, offline llm.encode/llm.score usage, or OpenAI embedding-style endpoint smoke tests."
disable-model-invocation: true
---

# vLLM Embeddings And Pooling

Use this sub-skill for non-generative vLLM runners and endpoint payloads. It covers embeddings, pooling, classification, reranking, and score-style workflows where output vectors or scores matter more than generated text.

## Use When

- The user wants `/v1/embeddings`, score/rerank endpoints, `llm.encode`, `llm.score`, pooling runners, or classification.
- The user needs payloads for vector stores, search, reranking, reward scoring, or non-generative evaluation.
- The user asks why a generative model does not behave like an embedding/reranker model.
- The user wants to smoke a retrieval endpoint through an OpenAI-compatible server.

## Inputs To Collect

- Task family, model ID, runner support, served model name, endpoint path, input batch size, maximum text length, and output schema.
- Whether normalization, pooling strategy, truncation, or pairwise scoring direction matters downstream.
- Server URL, auth, and whether the endpoint is offline Python or HTTP.

## Short Workflow

1. Determine whether the task is embedding, pooling, classification, reranking, or score.
2. Choose a model that supports the requested runner; generation models are not interchangeable with embedding/reranker models.
3. Read [references/workflows.md](references/workflows.md) for offline and server flow.
4. Read [references/pooling-reference.md](references/pooling-reference.md) for endpoint and payload differences.
5. Build payloads with bundled scripts, then smoke the selected endpoint with the server skill.
6. Validate output dimensions or score direction before integrating downstream.

## Bundled Scripts

- [scripts/make_embedding_payload.py](scripts/make_embedding_payload.py): writes `/v1/embeddings` request JSON.
- [scripts/score_payload.py](scripts/score_payload.py): writes score/reranker request JSON.

## References

- [references/workflows.md](references/workflows.md): embeddings/pooling/reranking workflow.
- [references/pooling-reference.md](references/pooling-reference.md): runners, endpoints, and validation notes.

## Boundaries

Use `vllm-openai-serving` for actual server lifecycle. Use `vllm-offline-inference` for text generation.

## Verification Notes

- Payload scripts are structural and safe without a model.
- Real endpoint validation requires a matching embedding/rerank/classification model, not a text-only smoke model.
- A Qwen text-generation smoke proves vLLM loads and serves text, but not embedding vector correctness.
