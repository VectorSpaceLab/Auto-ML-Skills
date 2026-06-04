---
name: sparse-encoder
description: "Use for SparseEncoder and SPLADE sparse embeddings, sparse semantic search, sparse similarity, sparsity statistics, token decoding, search-engine integration, and hybrid retrieval."
disable-model-invocation: true
---

# Sparse Encoder

Use this sub-skill for `sentence_transformers.SparseEncoder`: SPLADE-style sparse embeddings, sparse semantic search, sparse vector database integration, token-level interpretability, sparse training handoff, and hybrid retrieval with dense embeddings or Cross Encoder reranking.

Sparse Encoders produce high-dimensional vectors where most dimensions are zero. They can preserve lexical signals while adding semantic expansion, making them useful for interpretable and efficient retrieval systems.

## When To Use

Use this sub-skill when the user asks to:

- compute sparse embeddings with `SparseEncoder`;
- run sparse semantic search with dot product or model similarity;
- inspect active terms with `decode`, `intersection`, or `sparsity`;
- integrate sparse vectors with Qdrant, OpenSearch, Elasticsearch, Seismic, or SPLADE indexes;
- combine sparse and dense retrieval;
- use SPLADE, inference-free SPLADE, CSR, or sparse static embeddings.

Use `sentence-transformer` for dense embeddings and `cross-encoder` for reranking. Use `training-and-evaluation` for sparse losses and trainer workflows.

## Read These Files

Read [references/api-reference.md](references/api-reference.md) for verified `SparseEncoder` constructor, encode, similarity, sparsity, decode, save, and Hub-push signatures.

Read [references/workflows.md](references/workflows.md) for sparse embedding, semantic search, interpretability, vector search integration, and hybrid retrieval recipes.

Read [references/modeling-and-training-notes.md](references/modeling-and-training-notes.md) for SPLADE architectures, inference-free SPLADE, sparse modules, and training-loss handoff notes.

Read [references/troubleshooting.md](references/troubleshooting.md) for sparse tensor handling, unexpected score ranges, dense conversion problems, and sparse search integration issues.

Run or adapt [scripts/sparse_encoder_smoke.py](scripts/sparse_encoder_smoke.py) to verify sparse model loading, encoding, sparsity, and token decoding.

Run or adapt [scripts/sparse_search_template.py](scripts/sparse_search_template.py) for a small in-memory sparse search example.

## Short Workflow

1. Install the base package. Add search-engine client packages separately when integrating with Qdrant, OpenSearch, Elasticsearch, or other engines.
2. Load a model with `SparseEncoder(model_name_or_path, ...)`.
3. Encode documents with `encode_document` and queries with `encode_query`.
4. Keep sparse tensors sparse; avoid dense conversion for large corpora.
5. Use `semantic_search(..., score_function=model.similarity)` for small exact examples.
6. Use `model.decode` and `model.intersection` to inspect active terms and query-document token contributions.
7. For production retrieval, index sparse vectors in a search engine or vector database that supports sparse vectors.

## Minimal Sparse Example

```python
from sentence_transformers import SparseEncoder

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]
embeddings = model.encode(sentences)
print(embeddings.shape)
print(SparseEncoder.sparsity(embeddings))
print(model.decode(embeddings[0], top_k=5))
```

## Sparse Search Example

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.util import semantic_search

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
corpus = ["Neural networks learn representations.", "Mars rovers explore the planet."]
queries = ["How do artificial neural networks work?"]
corpus_embeddings = model.encode_document(corpus, convert_to_tensor=True)
query_embeddings = model.encode_query(queries, convert_to_tensor=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=2, score_function=model.similarity)
```

## Interpretability Pattern

```python
pointwise_scores = model.intersection(query_embeddings[0], corpus_embeddings)
for hit in hits[0]:
    terms = model.decode(pointwise_scores[hit["corpus_id"]], top_k=10)
    print(hit["score"], terms)
```

This shows which token dimensions contributed most to a sparse match.

## Hybrid Pattern

Use sparse retrieval for lexical-aware candidates, dense retrieval for semantic candidates, fuse candidate lists with reciprocal rank fusion or another strategy, then rerank the fused top-k with a `CrossEncoder`.

For evaluation and `ReciprocalRankFusionEvaluator`, use the training-and-evaluation sub-skill.
