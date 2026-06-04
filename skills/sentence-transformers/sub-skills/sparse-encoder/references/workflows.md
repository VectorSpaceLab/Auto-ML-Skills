# SparseEncoder Workflows

## Sparse Embeddings

```python
from sentence_transformers import SparseEncoder

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
embeddings = model.encode(["A sparse embedding example."], convert_to_sparse_tensor=True)
stats = SparseEncoder.sparsity(embeddings)
tokens = model.decode(embeddings[0], top_k=10)
```

Sparse vectors are often vocabulary-sized. High dimensionality is expected; most values should be zero.

## Prompt-Aware Sparse Retrieval

```python
corpus_embeddings = model.encode_document(corpus, convert_to_sparse_tensor=True)
query_embeddings = model.encode_query(queries, convert_to_sparse_tensor=True)
```

Use `encode_query` and `encode_document` even when a model appears prompt-free, because some sparse models define query/document prompts or router paths.

## In-Memory Sparse Search

```python
from sentence_transformers.util import semantic_search

hits = semantic_search(
    query_embeddings,
    corpus_embeddings,
    top_k=5,
    score_function=model.similarity,
)
```

This is appropriate for small examples and tests. Use a search engine for large corpora.

## Token Contribution Inspection

```python
pointwise = model.intersection(query_embeddings[0], corpus_embeddings)
for hit in hits[0]:
    print(hit["score"], corpus[hit["corpus_id"]])
    print(model.decode(pointwise[hit["corpus_id"]], top_k=10))
```

Use this to explain why a document matched a query. Active terms may include lexical expansions and subword tokens.

## Vector Database Integration

General pattern:

1. Encode documents with `encode_document(..., convert_to_sparse_tensor=True)`.
2. Convert sparse tensor representation into the target engine's sparse vector format.
3. Store sparse vectors with payload text and ids.
4. Encode queries with `encode_query`.
5. Search the sparse index.

The package has helper integrations for common search engines. External services and Python clients are not installed by the base package.

## Qdrant Pattern

Install `qdrant-client`. Encode corpus once, build or reuse an index, then query with sparse vectors. The package helper `semantic_search_qdrant` can manage an in-memory/local search flow for examples; production code should make collection and payload schema explicit.

## OpenSearch / Elasticsearch Pattern

Install the corresponding Python client and use sparse-vector capable index mappings. Keep the tokenizer vocabulary dimension and sparse vector format consistent with the search engine's expectations.

## Hybrid Dense + Sparse Retrieval

Use dense retrieval and sparse retrieval as complementary candidate generators:

1. Dense `SentenceTransformer` retrieves semantic candidates.
2. `SparseEncoder` retrieves lexical/expansion candidates.
3. Fuse ranks with reciprocal rank fusion or a weighted score rule.
4. Optionally rerank fused candidates with a `CrossEncoder`.

Evaluate each component separately before claiming hybrid improvement.

## Sparse Retrieve And Rerank

```python
from sentence_transformers import CrossEncoder

sparse_hits = semantic_search(query_embeddings, corpus_embeddings, top_k=50, score_function=model.similarity)[0]
candidate_ids = [hit["corpus_id"] for hit in sparse_hits]
candidate_docs = [corpus[i] for i in candidate_ids]
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
ranks = reranker.rank(query, candidate_docs)
```

Map reranked candidate indices back to original corpus ids.
