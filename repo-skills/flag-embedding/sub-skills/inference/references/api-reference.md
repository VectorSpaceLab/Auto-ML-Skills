# FlagEmbedding Inference API Reference

This reference summarizes the inference APIs future agents are most likely to use. It is self-contained and avoids depending on repository examples at runtime.

## Import Surface

```python
from FlagEmbedding import (
    FlagAutoModel,
    FlagAutoReranker,
    FlagModel,
    BGEM3FlagModel,
    FlagLLMModel,
    FlagICLModel,
    FlagPseudoMoEModel,
    FlagReranker,
    FlagLLMReranker,
    LayerWiseFlagLLMReranker,
    LightWeightFlagLLMReranker,
)
```

## Auto Embedder

Use `FlagAutoModel.from_finetuned(...)` when the checkpoint basename appears in FlagEmbedding's embedder mapping.

```python
model = FlagAutoModel.from_finetuned(
    "BAAI/bge-base-en-v1.5",
    normalize_embeddings=True,
    use_fp16=False,
    devices="cpu",
)
embeddings = model.encode(["I love NLP", "I love retrieval"])
```

Important parameters:

- `model_name_or_path`: Hugging Face model id or local checkpoint directory.
- `model_class`: explicit class selector for unmapped or renamed checkpoints; see `references/model-selection.md`.
- `normalize_embeddings`: normalizes embedding vectors when supported; with normalized vectors, dot product behaves like cosine similarity.
- `use_fp16` / `use_bf16`: precision controls; keep both false on CPU unless hardware support is known.
- `query_instruction_for_retrieval`: instruction applied by `encode_queries()`.
- `query_instruction_format`: two-slot format string, usually `"{}{}"` or an instruct format such as `"Instruct: {}\nQuery: {}"`.
- `devices`: `None`, string, integer, list of strings, or list of integers. Integers are converted to CUDA or MUSA device strings.
- `pooling_method`: `"cls"`, `"mean"`, or `"last_token"` depending on model architecture.
- `truncate_dim`: output dimension truncation for Matryoshka-style embeddings when supported.
- `batch_size`, `query_max_length`, `passage_max_length`, `convert_to_numpy`, and Hugging Face kwargs may be passed through to the concrete embedder.

## Embedder Methods

All embedder classes derive from the same base interface.

```python
queries = ["what is vector search?", "how does reranking work?"]
passages = ["Vector search compares embeddings.", "Rerankers score query-document pairs."]

q_vectors = model.encode_queries(queries, batch_size=32, max_length=128)
p_vectors = model.encode_corpus(passages, batch_size=32, max_length=512)
scores = q_vectors @ p_vectors.T
```

Method behavior:

- `encode(sentences, ...)` encodes raw sentences; if `instruction` is passed directly, it formats the text before encoding.
- `encode_queries(queries, ...)` uses `query_instruction_for_retrieval` and `query_instruction_format`.
- `encode_corpus(corpus, ...)` uses optional `passage_instruction_for_retrieval` and `passage_instruction_format` passed as kwargs at construction.
- `convert_to_numpy=True` returns NumPy arrays for normal embedders; `False` returns tensors where implemented.
- If more than one target device is configured and input is a list, the base class starts a multi-process pool.
- Call `stop_self_pool()` when long-running processes repeatedly create and destroy multi-device embedders.

## Concrete Embedders

- `FlagModel`: encoder-only dense embedder for classic BGE/E5/GTE-style models.
- `BGEM3FlagModel`: BGE-M3 multi-function embedder with dense, sparse, and optional ColBERT vectors.
- `FlagLLMModel`: decoder-only LLM embedder using last-token pooling.
- `FlagICLModel`: decoder-only in-context-learning embedder; accepts example-related kwargs such as `examples_for_task`.
- `FlagPseudoMoEModel`: decoder-only pseudo-MoE embedder for compatible checkpoints.

## BGE-M3 Outputs

`BGEM3FlagModel` and auto-loaded `encoder-only-m3` models return a dictionary, not a plain matrix, when using the M3-specific flags.

```python
outputs = model.encode(
    ["example text"],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)
dense = outputs["dense_vecs"]
lexical = outputs["lexical_weights"]
```

Common keys:

- `dense_vecs`: dense embedding matrix or vector.
- `lexical_weights`: sparse token-weight dictionaries.
- `colbert_vecs`: token-level multi-vector embeddings when `return_colbert_vecs=True`.

Scoring helpers:

- Dense score: `query_outputs["dense_vecs"] @ passage_outputs["dense_vecs"].T`.
- Sparse lexical score: `model.compute_lexical_matching_score(query_outputs["lexical_weights"], passage_outputs["lexical_weights"])`.
- Full BGE-M3 scoring: `model.compute_score(sentence_pairs, weights_for_different_modes=...)` where supported by the concrete class.

## Auto Reranker

Use `FlagAutoReranker.from_finetuned(...)` for mapped reranker checkpoints.

```python
reranker = FlagAutoReranker.from_finetuned(
    "BAAI/bge-reranker-base",
    use_fp16=False,
    devices="cpu",
    query_max_length=256,
    max_length=512,
)
score = reranker.compute_score(["what is panda?", "A panda is a bear species."])
```

Important parameters:

- `model_name_or_path`: Hugging Face model id or local checkpoint directory.
- `model_class`: explicit class selector for unmapped or renamed checkpoints.
- `use_fp16`: defaults false for rerankers; leave false on CPU.
- `trust_remote_code`: default comes from the mapping when auto-mapped; defaults false when `model_class` is explicit and not provided.
- `query_instruction_for_rerank`, `query_instruction_format`, `passage_instruction_for_rerank`, and `passage_instruction_format`: optional pair text formatting.
- `devices`, `batch_size`, `query_max_length`, `max_length`, and `normalize`: common runtime controls.

## Reranker Methods

```python
pairs = [
    ["what is panda?", "hi"],
    ["what is panda?", "The giant panda is a bear species endemic to China."],
]
raw_scores = reranker.compute_score(pairs)
probability_like_scores = reranker.compute_score(pairs, normalize=True)
```

Method behavior:

- A single pair may be passed as `[query, passage]` or `(query, passage)`.
- Multiple pairs should be a list of two-item pairs.
- `normalize=True` applies sigmoid normalization to map raw logits into `[0, 1]`-like scores.
- `query_max_length` truncates the query side when supported; `max_length` is the total or passage-inclusive limit depending on concrete reranker.
- Multi-device reranking starts a multi-process pool in the base class.

## Concrete Rerankers

- `FlagReranker`: encoder-only sequence-classification reranker, including BGE reranker base/large/v2-m3 style checkpoints.
- `FlagLLMReranker`: decoder-only reranker for compatible LLM reranker checkpoints.
- `LayerWiseFlagLLMReranker`: decoder-only layerwise reranker; pass `cutoff_layers=[...]` to `compute_score`.
- `LightWeightFlagLLMReranker`: decoder-only lightweight reranker; pass `cutoff_layers`, `compress_ratio`, and `compress_layers` as needed.

## Constructor Compatibility Notes

The installed package exposes these stable high-level signatures:

- `FlagAutoModel.from_finetuned(model_name_or_path, model_class=None, normalize_embeddings=True, use_fp16=True, use_bf16=False, query_instruction_for_retrieval=None, devices=None, pooling_method=None, trust_remote_code=None, query_instruction_format=None, truncate_dim=None, **kwargs)`
- `FlagAutoReranker.from_finetuned(model_name_or_path, model_class=None, use_fp16=False, trust_remote_code=None, **kwargs)`
- `AbsEmbedder.__init__(model_name_or_path, normalize_embeddings=True, use_fp16=True, use_bf16=False, query_instruction_for_retrieval=None, query_instruction_format="{}{}", devices=None, batch_size=256, query_max_length=512, passage_max_length=512, convert_to_numpy=True, truncate_dim=None, **kwargs)`
- `AbsReranker.__init__(model_name_or_path, use_fp16=False, query_instruction_for_rerank=None, query_instruction_format="{}{}", passage_instruction_for_rerank=None, passage_instruction_format="{}{}", devices=None, batch_size=128, query_max_length=None, max_length=512, normalize=False, **kwargs)`
