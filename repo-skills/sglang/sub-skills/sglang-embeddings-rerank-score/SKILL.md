---
name: sglang-embeddings-rerank-score
description: "Use SGLang embedding, classify, rerank, score, and reward-model endpoints and payloads."
disable-model-invocation: true
---

# SGLang Embeddings, Rerank, Score

Use this sub-skill for `/v1/embeddings`, `/v1/rerank`, `/v1/score`, `/v1/classify`, native `/encode`, native `/classify`, tokenization utilities, and reward model score extraction. It is for non-generative or scoring-style model serving, not normal chat generation.

Read [references/embeddings-rerank-score.md](references/embeddings-rerank-score.md) for endpoint payloads and model-type expectations. Use [scripts/validate_retrieval_payload.py](scripts/validate_retrieval_payload.py) to lint endpoint payloads before sending them to a server.

## Use When

- The user wants embeddings for search, retrieval, clustering, or vector stores.
- The user wants reranking, pair scoring, reward model outputs, classification, or tokenization/detokenization.
- The user asks why a chat model does not work on an embedding/rerank endpoint.
- The user needs an OpenAI-compatible payload shape for retrieval code.

## Inputs To Collect

- Endpoint family, model ID, whether the model is embedding/reranker/classifier/reward, and whether `--is-embedding` or equivalent mode is needed.
- Input count, maximum text length, desired normalization, batch size, and downstream vector schema.
- Server URL, model name exposed by `/v1/models`, auth, and expected output shape.

## Workflow

1. Confirm endpoint and model type: embedding, reranker, classifier, reward model, or score/logprob.
2. Launch embedding servers with `--is-embedding` when required by the model/endpoint.
3. Use OpenAI `/v1/embeddings` for client compatibility; native `/encode` for SGLang-specific features.
4. Check output shape and normalization expectations in downstream code.
5. For rerank/score, keep input pairs explicit and verify the score direction before using results for filtering.

## Verification

- Run the payload validator on a tiny example before using production text.
- Smoke `/v1/models`, then one endpoint-specific request with one or two inputs.
- Do not use a generative-only Qwen text model as proof that embedding/rerank endpoints are valid; use a matching retrieval/scoring model.

## Boundaries

Use `sglang-openai-server` for the base server process. Use `sglang-multimodal-serving` for image/audio/video embeddings or multimodal rerank. Use `sglang-cache-performance` only after endpoint correctness is established.
