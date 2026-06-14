---
name: reranking
description: "Use CrossEncoder models for pair scoring, reranking candidate documents, retrieve-and-rerank pipelines, pair classification, multimodal reranking, and CrossEncoder score troubleshooting."
---

# Reranking

Use this sub-skill for `CrossEncoder` workflows: pair scoring, reranking top-k candidates, pair classification, cross-modal reranking, and second-stage retrieval quality improvements.

## Required Reading

- `references/api-reference.md`: verified `CrossEncoder` signatures and score behavior.
- `references/workflows.md`: pair scoring, reranking, retrieve-and-rerank, and multimodal recipes.
- `scripts/rerank_candidates.py`: safe, self-contained reranking example.

For first-stage dense retrieval, read `../dense-embeddings/SKILL.md`. For sparse first-stage retrieval, read `../sparse-retrieval/SKILL.md`.

## When To Use CrossEncoder

Use `CrossEncoder` when the model should jointly inspect both sides of a pair:

- rerank top-k dense/sparse/BM25 candidates for a query;
- score `(sentence_a, sentence_b)` pairs for similarity or classification;
- rerank multimodal candidates when the model supports those modalities;
- improve precision on a candidate set where bi-encoder retrieval has high recall but noisy ordering.

Do not use `CrossEncoder` to search millions of documents directly. Retrieve candidates first, then rerank.

## Minimal Workflow

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
query = "How many people live in Berlin?"
passages = [
    "Berlin had a population of 3,520,031 registered inhabitants.",
    "Berlin is known for its museums.",
]

ranks = model.rank(query, passages, return_documents=True)
for row in ranks:
    print(row["score"], row["corpus_id"], row["text"])
```

Use `model.predict([(query, passage), ...])` when you need raw scores aligned to input pairs rather than sorted rank rows.

## Score Semantics

- Some models output logits, not probabilities. MS MARCO rerankers commonly do this.
- Ranking by logits is valid; sigmoid is monotonic and does not change order.
- If the user needs 0-1 scores, load with `activation_fn=torch.nn.Sigmoid()` or pass an activation for that call.
- For multiclass pair classification, use `num_labels` and `apply_softmax=True` as appropriate for the model.

## Practical Defaults

- Retrieve 50-200 candidates for many QA/search tasks, then rerank top 5-20 for display. Tune with evaluation.
- Use `batch_size` tuning for throughput; CrossEncoders are usually GPU-bound for larger batches.
- Keep query/candidate ids explicit when reranking candidates from a larger corpus.
- Use `top_k` in `rank` to reduce returned rows, but remember all provided candidates still need scoring unless you reduce the candidate list first.
- Use `return_documents=True` only when convenient; for large documents, keep ids and map externally.

## Common Pitfalls

- Forgetting that candidate ids returned by `rank` refer to the candidate list, not necessarily the original corpus.
- Applying sigmoid and then comparing scores with raw-logit thresholds from earlier code.
- Passing positional constructor args that now warn; use keyword args like `num_labels=`, `max_length=`, `activation_fn=`.
- Using a reranker model for the wrong domain or language; rerankers are task-sensitive.
