---
name: sparse-retrieval
description: "Use SparseEncoder and SPLADE models for sparse embeddings, sparse semantic search, token-level interpretability, Qdrant/OpenSearch sparse vector search, hybrid retrieval, and sparse retrieval troubleshooting."
---

# Sparse Retrieval

Use this sub-skill for `SparseEncoder` workflows: SPLADE-style sparse embeddings, sparse semantic search, interpretability with active tokens, sparse vector database integration, and hybrid dense+sparse retrieval.

## Required Reading

- `references/api-reference.md`: verified `SparseEncoder` signatures and sparse utility notes.
- `references/workflows.md`: manual sparse search, active-token interpretation, Qdrant/OpenSearch guidance, and hybrid retrieval.
- `scripts/sparse_semantic_search.py`: safe sparse search example.

Read `../reranking/SKILL.md` when sparse retrieval is only the first stage before CrossEncoder reranking.

## When To Use SparseEncoder

Use sparse retrieval when the user needs:

- learned sparse vectors over vocabulary dimensions;
- SPLADE-style semantic expansion with sparse index compatibility;
- interpretable token contributions;
- efficient inverted-index or sparse-vector search;
- hybrid search that combines dense semantic recall with lexical/sparse precision.

Use dense `SentenceTransformer` instead when the target vector store only supports dense vectors or when the model family/user requirement is dense embeddings.

## Minimal Workflow

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.util import semantic_search

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
corpus = [
    "Neural networks are inspired by biological networks.",
    "Mars rovers explore the surface of Mars.",
]
queries = ["How do artificial neural networks work?"]

corpus_embeddings = model.encode_document(corpus, convert_to_tensor=True, convert_to_sparse_tensor=True)
query_embeddings = model.encode_query(queries, convert_to_tensor=True, convert_to_sparse_tensor=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=2, score_function=model.similarity)
stats = SparseEncoder.sparsity(corpus_embeddings)
```

## Interpretability

Use `intersection` and `decode` to inspect which active tokens contributed to a sparse match:

```python
pointwise = model.intersection(query_embeddings[0], corpus_embeddings)
tokens = model.decode(pointwise[hits[0][0]["corpus_id"]], top_k=10)
```

This is useful for debugging why a sparse model retrieved a document.

## Practical Defaults

- Use `encode_query` and `encode_document` for retrieval; prompt-aware sparse models may need different query/document prompts.
- Use `convert_to_sparse_tensor=True` unless downstream code requires dense tensors.
- Use `SparseEncoder.sparsity` after encoding; sparse models should have high sparsity ratios.
- For sparse vector databases, install the relevant client and verify the server version/features separately.
- For hybrid retrieval, normalize and calibrate component scores on validation data instead of adding raw dense and sparse scores blindly.

## Common Pitfalls

- Treating sparse vectors like dense vectors in systems that do not preserve sparse indices.
- Forgetting that sparse dimensions correspond to tokenizer vocabulary ids, not human words unless decoded.
- Using a sparse model without matching the target search engine's sparse-vector schema.
- Judging sparse retrieval only by active dimension count; measure retrieval metrics and latency.
