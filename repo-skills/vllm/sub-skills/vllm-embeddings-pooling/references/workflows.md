# Embeddings And Pooling Workflows

## Offline

Use `llm.encode` for embedding/pooling models and `llm.score` for supported reranker/score models. Confirm signatures first:

```bash
python ../../scripts/inspect_api.py --object vllm:LLM
```

Generation models may not support pooling. Pick an embedding or cross-encoder model that vLLM supports.

## Server

Start server with an embedding/pooling model, then call `/v1/embeddings`:

```json
{"model": "BAAI/bge-small-en-v1.5", "input": ["hello", "world"]}
```

For score/rerank endpoints, inspect installed schemas and use `scripts/score_payload.py` to create a candidate request.

## Validation

- Output embeddings should be numeric vectors.
- Reranker outputs should contain scores per pair/query-document combination.
- If the endpoint returns generation output, the wrong model runner or endpoint was used.
