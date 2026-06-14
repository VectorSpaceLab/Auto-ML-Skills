# Inference Workflows

Read this for practical embedding, BGE-M3, reranking, custom checkpoint, and multi-device recipes.

## Dense Embedding Retrieval

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "BAAI/bge-base-en-v1.5",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages:",
    query_instruction_format="{}{}",
    use_fp16=True,
    devices=["cuda:0"],
)

queries = ["What is the capital of France?", "Who wrote Romeo and Juliet?"]
passages = [
    "Paris is the capital and most populous city of France.",
    "William Shakespeare wrote Romeo and Juliet.",
]

q = model.encode_queries(queries)
p = model.encode_corpus(passages)
scores = q @ p.T
print(scores)
```

Use `normalize_embeddings=True` unless the user has a reason to compare unnormalized vectors. If using CPU, set `use_fp16=False`.

## General Sentence Embeddings

Use `encode()` when there is no query/passage distinction:

```python
from FlagEmbedding import FlagModel

model = FlagModel("BAAI/bge-small-en-v1.5", use_fp16=False, devices="cpu")
embeddings = model.encode(["I love NLP", "I love retrieval"])
print(embeddings.shape)
```

## BGE-M3 Dense And Sparse Outputs

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True, devices=["cuda:0"])
out = model.encode(
    ["I love BGE", "I love text retrieval"],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)

print(out["dense_vecs"].shape)
print(out["lexical_weights"][0])
```

To score pairs directly:

```python
pairs = [
    ("what is BGE-M3?", "BGE-M3 supports dense, sparse, and multi-vector retrieval."),
]
scores = model.compute_score(pairs)
print(scores)
```

Use `return_colbert_vecs=True` only when downstream code can handle multi-vector outputs and the extra memory.

## Rerank Candidate Passages

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=True,
    devices=["cuda:0"],
)

query = "what is panda?"
passages = [
    "hi",
    "The giant panda is a bear species endemic to China.",
]
pairs = [[query, passage] for passage in passages]
scores = reranker.compute_score(pairs, normalize=True)
ranked = sorted(zip(passages, scores), key=lambda item: item[1], reverse=True)
print(ranked)
```

Use raw scores for model-internal comparisons and normalized scores when the user expects a 0-to-1 relevance score.

## Layerwise And Lightweight Rerankers

```python
from FlagEmbedding import LayerWiseFlagLLMReranker

reranker = LayerWiseFlagLLMReranker(
    "BAAI/bge-reranker-v2-minicpm-layerwise",
    use_fp16=True,
    devices=["cuda:0"],
)
scores = reranker.compute_score(
    [["query", "passage"]],
    cutoff_layers=[28],
)
```

For lightweight rerankers:

```python
from FlagEmbedding import LightWeightFlagLLMReranker

reranker = LightWeightFlagLLMReranker(
    "BAAI/bge-reranker-v2.5-gemma2-lightweight",
    use_fp16=True,
    devices=["cuda:0"],
)
scores = reranker.compute_score(
    [["query", "passage"]],
    cutoff_layers=[28],
    compress_ratio=2,
    compress_layers=[24, 40],
)
```

## Custom Checkpoints

When a checkpoint is not in the auto mapping:

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "/models/my-bge-checkpoint",
    model_class="encoder-only-base",
    pooling_method="cls",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages:",
    use_fp16=True,
    devices=["cuda:0"],
)
```

For BGE-M3-derived checkpoints use `model_class="encoder-only-m3"`. For decoder-only embeddings use `decoder-only-base`, `decoder-only-icl`, or `decoder-only-pseudo_moe`.

For custom rerankers:

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "/models/my-reranker",
    model_class="encoder-only-base",
    use_fp16=True,
    devices=["cuda:0"],
)
```

## Multi-Device Inference

Pass a list of devices:

```python
model = FlagAutoModel.from_finetuned(
    "BAAI/bge-base-en-v1.5",
    devices=["cuda:0", "cuda:1"],
)
```

When more than one target device is present and input is a list, the base classes start a multiprocessing pool. Stop it explicitly in long-running applications when the model is no longer needed:

```python
model.stop_self_pool()
```

## Hugging Face Transformers Fallback

Use raw Transformers only when the user needs custom tokenization/model code beyond FlagEmbedding wrappers. For normal encoder rerankers, `AutoModelForSequenceClassification` with paired inputs can reproduce direct reranker logits; for embedders, use `AutoModel` plus the model's pooling method. Prefer FlagEmbedding wrappers for ordinary BGE usage because they manage instructions, pooling defaults, and BGE-M3 modes.
