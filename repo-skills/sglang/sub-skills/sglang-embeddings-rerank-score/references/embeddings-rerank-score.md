# Embeddings, Rerank, Score Reference

## Embeddings

Launch:

```bash
python -m sglang.launch_server \
  --model-path <EMBEDDING_MODEL_ID> \
  --is-embedding \
  --host 127.0.0.1 --port 30000
```

OpenAI-compatible request:

```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:30000/v1", api_key="None")
resp = client.embeddings.create(model="<EMBEDDING_MODEL_ID>", input=["hello", "world"])
vectors = [item.embedding for item in resp.data]
```

Native endpoint: `POST /encode` with `text` or token IDs depending on model support.

## Rerank

Route: `/v1/rerank` accepts query/document style payloads for reranker models. Use `<RERANK_MODEL_ID>` and validate the model card for required input format. Multimodal rerank handlers can extract image/video content blocks when the reranker model supports them.

Generic payload shape:

```json
{
  "model": "<RERANK_MODEL_ID>",
  "query": "what is prefix caching?",
  "documents": ["doc one", "doc two"]
}
```

## Score And Reward Models

Inspected routes include `/v1/score` and examples for reward models. Score workflows are useful for reward modeling, pairwise ranking, and logprob-style evaluation. Confirm whether the target model is a reward/classification model or a language model used for logprob scoring.

## Classify

Routes: native `/classify` and OpenAI-compatible `/v1/classify`. Use when the model exposes classification behavior or when SGLang maps embedding-like outputs into class scores.

Tokenization utilities are exposed as `/v1/tokenize`, `/tokenize`, `/v1/detokenize`, and `/detokenize`; they are useful for score/debug workflows but are not substitutes for embedding or rerank endpoints.

## Pitfalls

- Text-generation models generally do not become embedding models without `--is-embedding` and compatible architecture.
- Embedding vector dimension is model-specific; assert it in tests.
- Rerank payload names can vary across client conventions; keep server smoke tests close to the actual SGLang route.
