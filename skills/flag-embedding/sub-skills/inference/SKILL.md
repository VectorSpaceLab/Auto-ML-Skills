---
name: inference
description: "Helps agents run FlagEmbedding embedder and reranker inference, including BGE-M3 dense/sparse outputs and LLM rerankers."
disable-model-invocation: true
---

# FlagEmbedding Inference

Use this sub-skill when the user needs embeddings, retrieval similarity scores, reranker relevance scores, model selection for inference, or API-level help for `FlagAutoModel`, `BGEM3FlagModel`, `FlagAutoReranker`, and related classes.

## Start Here

1. Identify whether the task needs embeddings or direct reranker scores.
2. Choose a model and class using the root [../../references/model-overview.md](../../references/model-overview.md).
3. Use `FlagAutoModel.from_finetuned(...)` or `FlagAutoReranker.from_finetuned(...)` for mapped models.
4. For local checkpoints or unmapped names, pass `model_class` explicitly.
5. Keep smoke tests small. Loading real models can download large weights.

## Embedding Workflows

For standard dense embeddings, read [references/embedder-api.md](references/embedder-api.md). It includes verified signatures and examples for `FlagAutoModel`, `FlagModel`, `BGEM3FlagModel`, `FlagLLMModel`, `FlagICLModel`, and `FlagPseudoMoEModel`.

Minimal dense retrieval pattern:

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "BAAI/bge-base-en-v1.5",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ",
    use_fp16=True,
)
queries = ["what is bge?"]
passages = ["BGE is a family of retrieval embedding models."]
q = model.encode_queries(queries)
p = model.encode_corpus(passages)
scores = q @ p.T
```

For BGE-M3 multi-function outputs:

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
emb = model.encode(
    ["FlagEmbedding supports dense, sparse, and ColBERT vectors."],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=True,
)
```

## Reranking Workflows

For cross-encoder and LLM reranking, read [references/reranker-api.md](references/reranker-api.md). It includes verified signatures and examples for `FlagAutoReranker`, `FlagReranker`, `FlagLLMReranker`, `LayerWiseFlagLLMReranker`, and `LightWeightFlagLLMReranker`.

Minimal reranking pattern:

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=True,
)
pairs = [
    ["what is panda?", "hi"],
    ["what is panda?", "The giant panda is a bear species endemic to China."],
]
scores = reranker.compute_score(pairs)
normalized = reranker.compute_score(pairs, normalize=True)
```

Layerwise and lightweight rerankers accept extra score-time arguments such as `cutoff_layers`, `compress_ratio`, and `compress_layers`.

## Scripts

Run [scripts/smoke_inference_no_download.py](scripts/smoke_inference_no_download.py) when you need to validate imports, signatures, and model mapping without downloading any model.

Read or adapt [scripts/build_rag_rerank_example.py](scripts/build_rag_rerank_example.py) when constructing a small retrieval-plus-reranking Python script. It is intentionally a template and only downloads models when the user runs it with real model names.

## Common Decisions

Use `encode_queries()` for retrieval queries when query instructions should be applied automatically. Use `encode_corpus()` for passages; they normally do not receive retrieval query instructions.

Use `normalize_embeddings=True` for inner-product retrieval over normalized embeddings. If embeddings are not normalized, inner product and cosine similarity differ.

Use `return_dense`, `return_sparse`, and `return_colbert_vecs` with `BGEM3FlagModel` only when the downstream index or scorer can consume the requested representation.

Use rerankers after an initial retriever has selected a manageable top-k. Rerankers score query/passage pairs directly and are usually much slower than vector search.

## Troubleshooting

Read [references/troubleshooting.md](references/troubleshooting.md) for inference-specific failure modes: auto mapping misses, trust-remote-code, precision/device errors, score normalization, and M3 output shape confusion.

Also read the root [../../references/troubleshooting.md](../../references/troubleshooting.md) for package-level install and dependency failures.
