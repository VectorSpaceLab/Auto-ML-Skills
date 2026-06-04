---
name: sentence-transformer
description: "Use for SentenceTransformer dense or multimodal embeddings, semantic search, similarity, clustering, paraphrase mining, custom embedding models, and prompt-aware query/document encoding."
disable-model-invocation: true
---

# Sentence Transformer

Use this sub-skill for first-stage embedding models: text embeddings, multimodal embeddings, similarity scores, dense semantic search, clustering, paraphrase mining, image search, and custom embedding model composition.

The main class is `sentence_transformers.SentenceTransformer`. It encodes each input independently, so document embeddings can be precomputed and indexed.

## When To Use

Use this sub-skill when the user asks to:

- compute embeddings for text, image, audio, video, or mixed-modal inputs;
- compare text similarity or build semantic textual similarity workflows;
- retrieve documents with dense vectors before an optional reranker;
- cluster, deduplicate, mine paraphrases, or find communities;
- use `encode_query` and `encode_document` with prompt-aware retrieval models;
- build or inspect a custom `SentenceTransformer` module chain.

Use the `cross-encoder` sub-skill instead when the task scores pairs jointly or reranks a small candidate set. Use `sparse-encoder` when the user explicitly needs sparse vectors, SPLADE, lexical interpretability, or sparse vector search.

## Read These Files

Read [references/api-reference.md](references/api-reference.md) for verified signatures and return-type behavior for `SentenceTransformer`, dense retrieval utilities, similarity functions, and save/push methods.

Read [references/workflows.md](references/workflows.md) for task recipes: embeddings, prompt-aware retrieval, semantic search, retrieve-and-rerank handoff, clustering, paraphrase mining, and multimodal inputs.

Read [references/custom-models.md](references/custom-models.md) when composing modules such as `Transformer`, `Pooling`, `Dense`, `Normalize`, `StaticEmbedding`, or multimodal `Router` models.

Read [references/troubleshooting.md](references/troubleshooting.md) for wrong scores, prompt confusion, modality errors, memory issues, and model-loading pitfalls.

Run or adapt [scripts/dense_embedding_smoke.py](scripts/dense_embedding_smoke.py) to verify that a selected embedding model can load, encode, and compute similarities.

Run or adapt [scripts/dense_semantic_search_template.py](scripts/dense_semantic_search_template.py) for a small local semantic-search example without external datasets.

## Short Workflow

1. Install the base package; add `image`, `audio`, or `video` extras for non-text inputs.
2. Load a model with `SentenceTransformer(model_name_or_path, ...)`.
3. For retrieval, encode queries with `encode_query` and corpus items with `encode_document`; for generic embeddings, use `encode`.
4. Set `normalize_embeddings=True` when using dot-product ANN indexes as cosine-like retrieval.
5. Use `model.similarity(...)` for pairwise matrices, or `sentence_transformers.util.semantic_search(...)` for top-k hits over tensors.
6. For large corpora, precompute corpus embeddings once and move from exact search to FAISS, hnswlib, Annoy, Elasticsearch, OpenSearch, or another vector database.
7. For higher final precision, pass only the top retrieved candidates to a `CrossEncoder` reranker.

## Minimal Dense Example

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]
embeddings = model.encode(sentences)
similarities = model.similarity(embeddings, embeddings)
print(embeddings.shape)
print(similarities)
```

## Retrieval Pattern

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
documents = ["Python is a programming language.", "Mars is called the Red Planet."]
doc_embeddings = model.encode_document(documents, normalize_embeddings=True)
query_embeddings = model.encode_query(["What is Python?"], normalize_embeddings=True)
hits = semantic_search(query_embeddings, doc_embeddings, top_k=2)
```

Use `encode_query` and `encode_document` even when they behave like `encode`; they preserve prompt/task routing for models that need it.

## Multimodal Notes

Some `SentenceTransformer` models support images, audio, video, or chat-message inputs. Verify support before encoding:

```python
print(model.modalities)
print(model.supports("image"))
```

Text inputs are strings. Images can be PIL images, local paths, URLs, or arrays depending on the model and dependencies. Audio/video support requires the appropriate extras and sometimes `torchcodec` for decoder objects.

## Common Decisions

Use symmetric retrieval models when query and document are the same kind of text, such as duplicate-question search.

Use asymmetric retrieval models when short queries search longer passages or answers; these models often need query/document prompts.

Use dense embedding quantization or Matryoshka truncation when the main bottleneck is vector storage or search cost; use ONNX/OpenVINO when the model forward pass is the bottleneck.

Do not use a Cross Encoder over a large corpus. Dense retrieval is the scalable candidate generator; Cross Encoders rerank the top candidates.
