# Reranking Workflows

Read this for practical CrossEncoder patterns.

## Pair Scoring

Use `predict` when you need scores in input order.

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/stsb-distilroberta-base")
pairs = [
    ("A man is eating pasta.", "A person eats food."),
    ("A man is eating pasta.", "A child is playing outside."),
]
scores = model.predict(pairs)
```

## Rerank Candidate Documents

Use `rank` when you have one query and a list of candidate documents.

```python
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
ranks = model.rank(query, candidates, top_k=10)
for row in ranks:
    original_id = candidate_ids[row["corpus_id"]]
    print(row["score"], original_id)
```

Keep `candidate_ids` from the first-stage retriever; `corpus_id` is local to the candidate list.

## Retrieve And Rerank With Dense Retrieval

```python
from sentence_transformers import CrossEncoder, SentenceTransformer
from sentence_transformers.util import semantic_search

retriever = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

corpus_embeddings = retriever.encode_document(corpus, convert_to_tensor=True, normalize_embeddings=True)
query_embeddings = retriever.encode_query([query], convert_to_tensor=True, normalize_embeddings=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=100)[0]

candidate_ids = [hit["corpus_id"] for hit in hits]
candidates = [corpus[idx] for idx in candidate_ids]
ranked = reranker.rank(query, candidates, top_k=10)
final = [(row["score"], candidate_ids[row["corpus_id"]], corpus[candidate_ids[row["corpus_id"]]]) for row in ranked]
```

## Rerank BM25 Or Sparse Results

The first stage does not need to be dense. Any candidate list works:

```python
candidates = bm25_results[:100]  # or sparse/vector DB hits
ranked = reranker.rank(query, [doc["text"] for doc in candidates], top_k=10)
```

## Scores Between 0 And 1

For logit rerankers where the user wants probability-like scores:

```python
import torch
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", activation_fn=torch.nn.Sigmoid())
scores = model.predict([(query, passage) for passage in passages])
```

Do not use a fixed threshold from another model without calibrating on validation data.

## Multimodal Reranking

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("Qwen/Qwen3-VL-Reranker-2B")
assert model.supports(("text", "image"))
ranks = model.rank(
    "A green car parked near a building",
    ["car.jpg", {"text": "A city car", "image": "car.jpg"}, "A flower photo"],
)
```

Install the needed extras and avoid remote URL/image inputs in automated tests unless network access is expected.

## Evaluation Habit

For search systems, evaluate the whole retrieve-and-rerank pipeline, not only CrossEncoder pair accuracy. Track recall at the candidate stage and nDCG/MRR after reranking.
