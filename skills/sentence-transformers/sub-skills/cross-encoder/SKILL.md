---
name: cross-encoder
description: "Use for CrossEncoder pair scoring, reranking, pair classification, multimodal rerankers, logits versus probabilities, and second-stage retrieve-and-rerank pipelines."
disable-model-invocation: true
---

# Cross Encoder

Use this sub-skill for `sentence_transformers.CrossEncoder`: pairwise scoring, reranking retrieved documents, pair classification, reranker fine-tuning handoff, multimodal rerankers, and understanding raw logits versus probabilities.

Cross Encoders score pairs jointly. They are often more accurate than dense or sparse retrievers for a small candidate set, but they are slower because each query-document pair requires a model forward pass.

## When To Use

Use this sub-skill when the user asks to:

- score sentence pairs, query-passage pairs, image-text pairs, or other pairable inputs;
- rerank top-k candidates returned by dense, sparse, BM25, or hybrid retrieval;
- use `CrossEncoder.predict` or `CrossEncoder.rank`;
- interpret MS MARCO Cross Encoder scores and logits;
- build pair classifiers such as NLI or duplicate detection;
- inspect or compose encoder-based and causal-LM-based reranker modules.

Use the `sentence-transformer` or `sparse-encoder` sub-skills for first-stage retrieval over large corpora. Use `training-and-evaluation` for fine-tuning losses, datasets, and evaluators.

## Read These Files

Read [references/api-reference.md](references/api-reference.md) for verified constructor, `predict`, `rank`, `fit`, save, and Hub-push signatures.

Read [references/workflows.md](references/workflows.md) for pair scoring, reranking, retrieve-and-rerank, pair classification, multimodal inputs, and score calibration patterns.

Read [references/custom-models.md](references/custom-models.md) when working with encoder sequence-classification rerankers, causal-LM rerankers, `LogitScore`, custom true/false tokens, or saved model layout.

Read [references/troubleshooting.md](references/troubleshooting.md) for raw logits, activation functions, slow reranking, pair formatting, and backend/export differences.

Run or adapt [scripts/cross_encoder_smoke.py](scripts/cross_encoder_smoke.py) to verify that a reranker can load and rank a tiny in-memory passage list.

Run or adapt [scripts/retrieve_rerank_template.py](scripts/retrieve_rerank_template.py) for a compact dense-retrieve then cross-rerank pipeline.

## Short Workflow

1. Load a reranker with `CrossEncoder(model_name_or_path, ...)`.
2. For explicit pairs, call `predict([(a, b), ...])`.
3. For one query against many documents, call `rank(query, documents, top_k=..., return_documents=True)`.
4. Keep candidate sets small; use dense, sparse, lexical, or hybrid retrieval before reranking.
5. If scores need probabilities, pass `activation_fn=torch.nn.Sigmoid()` or `apply_softmax=True` for multi-label/class outputs as appropriate.
6. Do not globally apply sigmoid when the only task is ranking; monotonic transforms do not change order.

## Minimal Pair Scoring

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
pairs = [
    ("How many people live in Berlin?", "Berlin has about 3.5 million registered inhabitants."),
    ("How many people live in Berlin?", "Berlin is known for museums."),
]
scores = model.predict(pairs)
print(scores)
```

## Minimal Ranking

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
query = "How many people live in Berlin?"
passages = [
    "Berlin had a population of about 3.5 million registered inhabitants.",
    "Berlin has many museums.",
    "Paris is the capital of France.",
]
ranks = model.rank(query, passages, return_documents=True)
for row in ranks:
    print(row["score"], row["corpus_id"], row["text"])
```

## Score Semantics

Many MS MARCO rerankers return raw logits, not calibrated probabilities in `[0, 1]`. Raw logits are fine for ranking.

For probability-like output:

```python
import torch
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", activation_fn=torch.nn.Sigmoid())
```

or pass `activation_fn=torch.nn.Sigmoid()` to `predict` or `rank`.

## Multimodal Notes

Some Cross Encoders support image, video, or message-like inputs. Verify support:

```python
print(model.modalities)
print(model.supports(("image", "text")))
```

Each pair element can be a string, image path/URL/PIL object, or multimodal dict depending on the model.

## Performance Rule

A Cross Encoder is a second-stage model. First retrieve 20-200 candidates, then rerank. Scoring every document in a large corpus is the common performance mistake.
