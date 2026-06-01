# CrossEncoder Workflows

## Pair Scoring

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/stsb-distilroberta-base")
pairs = [
    ("A man is eating pasta.", "A person eats food."),
    ("A man is eating pasta.", "The sky is blue."),
]
scores = model.predict(pairs)
```

Use this for STS pair scoring, binary relevance scoring, or pair classification. Check the model card for score scale.

## Ranking Documents For One Query

```python
query = "How many people live in Berlin?"
passages = [
    "Berlin has about 3.5 million registered inhabitants.",
    "Berlin is famous for museums.",
    "Paris is in France.",
]
ranks = model.rank(query, passages, top_k=3, return_documents=True)
```

Use `rank` rather than manually constructing pairs when one query is scored against many documents.

## Retrieve And Rerank

1. Use a dense, sparse, lexical, or hybrid retriever to get candidate ids.
2. Slice the original documents by those ids.
3. Pass candidates to `CrossEncoder.rank`.
4. Map `corpus_id` back through the candidate ids if needed.

```python
candidate_ids = [hit["corpus_id"] for hit in dense_hits[0][:50]]
candidate_docs = [corpus[i] for i in candidate_ids]
ranks = reranker.rank(query, candidate_docs)
final = [
    {
        "corpus_id": candidate_ids[row["corpus_id"]],
        "rerank_score": row["score"],
        "text": corpus[candidate_ids[row["corpus_id"]]],
    }
    for row in ranks
]
```

## Logits To Probabilities

For binary relevance where users require probabilities:

```python
import torch
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
scores = model.predict(pairs, activation_fn=torch.nn.Sigmoid())
```

For multi-class classification:

```python
probs = model.predict(pairs, apply_softmax=True)
```

Do not interpret all reranker scores as calibrated probabilities; many are ranking logits.

## Pair Classification

Initialize with `num_labels` when starting from a generic encoder checkpoint:

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("google-bert/bert-base-uncased", num_labels=3)
```

Use `CrossEntropyLoss` and classification evaluators during training. See the training sub-skill for data formats.

## Multimodal Reranking

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("Qwen/Qwen3-VL-Reranker-2B")
print(model.supports(("image", "text")))

query = "A green car parked near a building"
documents = [
    "path/to/car.jpg",
    {"text": "A city car", "image": "path/to/car.jpg"},
    "A text-only passage.",
]
ranks = model.rank(query, documents)
```

Install `sentence-transformers[image]`, `[audio]`, or `[video]` as needed. Support depends on the model, not just the package extra.

## Backend Use

For ONNX:

```python
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", backend="onnx")
```

If exporting occurs on first load, save the model directory or push a PR to avoid repeated conversion. See the optimization sub-skill.

## Candidate Count Guidance

Typical rerank candidate counts are 20-200 depending on latency and model size. If a user asks to rerank millions of documents, add a first-stage retrieval/indexing step.
