---
name: inference
description: "Use for FlagEmbedding inference: embedding vectors, BGE-M3 dense/sparse/ColBERT outputs, reranking scores, model-class selection, device settings, and inference troubleshooting."
---

# FlagEmbedding Inference

Use this sub-skill when the user wants to embed text, compare query and passage vectors, rerank documents, choose a BGE or reranker model, inspect API signatures, or debug inference behavior.

## Before Running Inference

Install inference dependencies:

```bash
python -m pip install -U FlagEmbedding
```

Check the environment without downloading models:

```bash
python ../../scripts/check_flagembedding_env.py --show-torch
```

Read:

- `references/api-reference.md` for verified signatures, model-class values, return types, and parameter notes.
- `references/workflows.md` for task-oriented embedder, BGE-M3, reranker, multi-device, and custom-checkpoint recipes.
- `references/troubleshooting.md` for model mapping errors, result-shape surprises, dtype/device failures, and slow/memory-heavy inference.

Run or adapt:

- `scripts/inference_smoke_test.py` to perform no-download import checks by default, or optional real-model embedding/reranking checks when the user provides model ids or local model paths.

## Choose The API

- Use `FlagAutoModel.from_finetuned(...)` for embedders when the model id is known by the package or when you can provide explicit `model_class`.
- Use `FlagModel` for encoder-only dense embedders such as BGE v1/v1.5.
- Use `BGEM3FlagModel` for BGE-M3 dense, sparse lexical, and ColBERT-style vectors.
- Use `FlagLLMModel` for decoder-only embedding models.
- Use `FlagICLModel` for in-context-learning embedding models.
- Use `FlagAutoReranker.from_finetuned(...)` for rerankers when auto mapping or explicit `model_class` is appropriate.
- Use `FlagReranker`, `FlagLLMReranker`, `LayerWiseFlagLLMReranker`, or `LightWeightFlagLLMReranker` when the model family is already known.

## Minimal Embedder Pattern

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "BAAI/bge-base-en-v1.5",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages:",
    use_fp16=True,
    devices=["cuda:0"],
)

queries = ["What is the capital of France?"]
passages = ["Paris is the capital and most populous city of France."]
q_vecs = model.encode_queries(queries)
p_vecs = model.encode_corpus(passages)
scores = q_vecs @ p_vecs.T
print(scores)
```

Use `encode_queries()` for query-side instructions and `encode_corpus()` for passage-side encoding. Use `encode()` for general sentence embedding when no retrieval-specific query instruction should be applied.

## Minimal Reranker Pattern

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=True,
    devices=["cuda:0"],
)

pairs = [
    ["what is panda?", "hi"],
    ["what is panda?", "The giant panda is a bear species endemic to China."],
]
scores = reranker.compute_score(pairs, normalize=True)
print(scores)
```

Raw reranker scores are model-dependent. Use `normalize=True` when the user wants sigmoid-mapped scores.

## Custom Or Local Checkpoints

If auto loading cannot infer a class from the model directory or model id, pass `model_class` explicitly:

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "path-or-model-id",
    model_class="encoder-only-base",
    pooling_method="cls",
    trust_remote_code=False,
)
```

For rerankers:

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "path-or-model-id",
    model_class="encoder-only-base",
)
```

## Verification

For a no-download verification:

```bash
python scripts/inference_smoke_test.py --mode import
```

For a real embedding model check, only after the user accepts model loading/download:

```bash
python scripts/inference_smoke_test.py \
  --mode embedder \
  --embedder BAAI/bge-base-en-v1.5 \
  --device cuda:0 \
  --query "What is the capital of France?" \
  --passage "Paris is the capital of France."
```

For a reranker check:

```bash
python scripts/inference_smoke_test.py \
  --mode reranker \
  --reranker BAAI/bge-reranker-v2-m3 \
  --device cuda:0 \
  --query "What is the capital of France?" \
  --passage "Paris is the capital of France."
```
