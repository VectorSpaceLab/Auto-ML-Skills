---
name: dense-embeddings
description: "Use SentenceTransformer dense embedding models for encode, encode_query, encode_document, semantic similarity, semantic search, clustering, paraphrase mining, multimodal embeddings, and dense retrieval troubleshooting."
---

# Dense Embeddings

Use this sub-skill for `SentenceTransformer` bi-encoder workflows: computing embeddings, semantic textual similarity, dense semantic search, clustering, paraphrase mining, multimodal embedding search, or first-stage retrieval before reranking.

## Required Reading

- `references/api-reference.md`: verified `SentenceTransformer` and dense utility signatures.
- `references/workflows.md`: dense embedding, semantic search, paraphrase mining, clustering, multimodal, and retrieval patterns.
- `scripts/dense_semantic_search.py`: safe, self-contained dense search example. Run or adapt it when the user asks for a minimal working implementation.

Also read root `../../references/troubleshooting.md` for install, download, scoring, and backend issues.

## Choose The Encoding Method

| Task | Method | Why |
| --- | --- | --- |
| symmetric STS, clustering, classification features, dedup | `model.encode(...)` | General embedding path. |
| asymmetric retrieval query | `model.encode_query(...)` | Uses a model's query prompt and Router task when available. |
| asymmetric retrieval documents/passages | `model.encode_document(...)` | Uses document/passage/corpus prompt and Router task when available. |
| token-level outputs | `model.encode(..., output_value="token_embeddings")` | Returns token embeddings instead of pooled vectors. |
| GPU similarity with exact search | `convert_to_tensor=True` | Keeps embeddings as torch tensors for GPU scoring. |
| normalized dot-product search | `normalize_embeddings=True` plus `dot_score` | Dot product becomes equivalent to cosine and can be faster. |

If the user does not know whether the retrieval task is symmetric or asymmetric, ask about query/document lengths and content. Short questions against longer passages usually mean asymmetric retrieval.

## Minimal Workflow

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Neural networks are inspired by biological nervous systems.",
    "Mars rovers explore the surface of Mars.",
    "Wind and solar are renewable energy sources.",
]
queries = ["How do artificial neural networks work?"]

corpus_embeddings = model.encode_document(corpus, convert_to_tensor=True, normalize_embeddings=True)
query_embeddings = model.encode_query(queries, convert_to_tensor=True, normalize_embeddings=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=3)

for hit in hits[0]:
    print(hit["score"], corpus[hit["corpus_id"]])
```

For pure STS or clustering, use `model.encode` for all texts instead of query/document methods.

## Practical Defaults

- Start with a model trained for the task. General STS models can be weak for QA retrieval; MS MARCO or retrieval-tuned models are usually better for short-query/long-document search.
- Use `batch_size` tuning for throughput. Increase until memory is close to the limit, then back off.
- For large exact search, lower `query_chunk_size` and `corpus_chunk_size` if `semantic_search` runs out of memory.
- For million-scale or low-latency search, encode once, normalize/store vectors, and use FAISS, hnswlib, Annoy, Elasticsearch, OpenSearch, Qdrant, or another vector database.
- For multimodal models, install the required extra and inspect `model.modalities`/`model.supports(...)` before shaping inputs.
- Do not pass `trust_remote_code=True` unless the user explicitly trusts that model repository; pin a `revision` for reproducibility.

## Output Shapes And Types

- `convert_to_numpy=True` and `convert_to_tensor=False` returns numpy arrays for sentence embeddings.
- `convert_to_tensor=True` returns a torch tensor.
- A single string input may return a single vector rather than a batch-shaped list; wrap in a list when consistent batch shape matters.
- `precision` can be `float32`, `int8`, `uint8`, `binary`, or `ubinary`; use lower precision deliberately and validate recall.

## Common Pitfalls

- Do not use CrossEncoder over an entire large corpus; use dense embeddings to retrieve candidates first.
- Do not use `encode` blindly for prompt-tuned retrieval models when the query/document distinction matters.
- Do not compare vectors from different models or incompatible prompt settings.
- Persist corpus embeddings and model id/version together so future queries use the same representation.
- If scores look shifted after quantization/truncation, measure ranking metrics, not only raw score similarity.
