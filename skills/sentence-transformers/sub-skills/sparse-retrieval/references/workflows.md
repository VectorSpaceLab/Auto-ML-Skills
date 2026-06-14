# Sparse Retrieval Workflows

Read this for SPLADE and sparse vector search patterns.

## Manual Sparse Search

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.util import semantic_search

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
corpus_embeddings = model.encode_document(corpus, convert_to_tensor=True, convert_to_sparse_tensor=True)
query_embeddings = model.encode_query(queries, convert_to_tensor=True, convert_to_sparse_tensor=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=10, score_function=model.similarity)
```

This is useful for prototypes and small-to-medium exact search. For production, index sparse vectors in a system that can exploit sparsity.

## Explain A Sparse Hit

```python
query_id = 0
hit = hits[query_id][0]
pointwise_scores = model.intersection(query_embeddings[query_id], corpus_embeddings)
tokens = model.decode(pointwise_scores[hit["corpus_id"]], top_k=10)
for token, value in tokens:
    print(token, value)
```

Use this when a user asks why a sparse model retrieved a document or when tuning query/document prompts.

## Qdrant Sparse Search

Prerequisites:

```bash
pip install qdrant-client
```

The Qdrant service must be running or accessible. Use `semantic_search_qdrant` for a reusable in-memory index object:

```python
from sentence_transformers.sparse_encoder.search_engines import semantic_search_qdrant

results, search_time, corpus_index = semantic_search_qdrant(
    query_embeddings,
    corpus_index=corpus_index,
    corpus_embeddings=corpus_embeddings if corpus_index is None else None,
    top_k=5,
    output_index=True,
)
```

Store `corpus_index` for repeated queries. Do not rebuild the index for every query in production.

## OpenSearch Sparse Search

Prerequisites:

```bash
pip install opensearch-py
```

The OpenSearch server and sparse vector mapping must match the helper's expected schema. Use `semantic_search_opensearch` when the service is configured.

OpenSearch-specific SPLADE models may use Router modules with separate query/document components; verify prompts and modules before adapting examples.

## Hybrid Dense And Sparse Retrieval

A typical hybrid system:

1. Encode dense vectors with `SentenceTransformer`.
2. Encode sparse vectors with `SparseEncoder`.
3. Search both indexes.
4. Merge candidates by reciprocal rank fusion, weighted score sum, or learned fusion.
5. Optionally rerank the merged candidate set with `CrossEncoder`.

Do not add raw dense cosine scores and sparse dot scores without calibration. Use validation data to tune weights.

## Sparse Model Health Checks

After encoding, inspect:

```python
stats = SparseEncoder.sparsity(corpus_embeddings)
print(stats["active_dims"], stats["sparsity_ratio"])
```

Also inspect a few decoded vectors:

```python
print(model.decode(corpus_embeddings[0], top_k=20))
```

If vectors have unexpectedly many active dimensions or nonsensical active tokens, check model choice, prompts, `max_active_dims`, and preprocessing.
