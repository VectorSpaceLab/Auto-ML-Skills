# SentenceTransformer Workflows

Use these recipes as starting points for common dense and multimodal embedding tasks.

## Dense Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = ["A small example.", "Another sentence."]
embeddings = model.encode(texts, batch_size=32)
```

For feature extraction into another ML model, keep default NumPy output. For torch pipelines, set `convert_to_tensor=True`.

## Semantic Textual Similarity

```python
sentences = ["A man is eating pasta.", "A person eats food.", "The sky is blue."]
embeddings = model.encode(sentences, convert_to_tensor=True)
scores = model.similarity(embeddings, embeddings)
```

Use cosine similarity for most general embedding models unless the model card says otherwise.

## Prompt-Aware Retrieval

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search, dot_score

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
corpus = ["Python is a programming language.", "Mars is a planet."]
queries = ["What is Python?"]

corpus_embeddings = model.encode_document(corpus, normalize_embeddings=True, convert_to_tensor=True)
query_embeddings = model.encode_query(queries, normalize_embeddings=True, convert_to_tensor=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=3, score_function=dot_score)
```

Use `encode_query` and `encode_document` for asymmetric search and any model that defines prompts or a `Router`.

## Symmetric Versus Asymmetric Search

Symmetric search means query and corpus entries are the same type and length, such as duplicate-question search. General STS or question-similarity embedding models are appropriate.

Asymmetric search means short queries search longer passages or documents. Use retrieval-tuned models and query/document encoders.

If the user reports poor retrieval quality, first verify that model choice matches symmetric/asymmetric task shape before changing indexes or thresholds.

## Exact Dense Search

`semantic_search` is convenient for small and medium corpora. It chunks queries and corpus vectors and returns top-k hits:

```python
from sentence_transformers.util import semantic_search

hits = semantic_search(query_embeddings, corpus_embeddings, top_k=10)
for hit in hits[0]:
    print(hit["corpus_id"], hit["score"])
```

For large corpora, use an ANN/vector database and store corpus embeddings once.

## Retrieve And Rerank

Dense retrievers should generate candidates. Cross Encoders should rerank candidates:

```python
from sentence_transformers import CrossEncoder

candidate_ids = [hit["corpus_id"] for hit in hits[0][:50]]
candidate_docs = [corpus[i] for i in candidate_ids]
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
ranks = reranker.rank(queries[0], candidate_docs, return_documents=True)
```

Keep the reranker candidate set small enough for latency and cost constraints.

## Clustering And Community Detection

Use embeddings with scikit-learn for k-means/agglomerative clustering:

```python
from sklearn.cluster import KMeans

embeddings = model.encode(texts)
labels = KMeans(n_clusters=5, n_init="auto").fit_predict(embeddings)
```

Use `community_detection` when the task is "find groups above a similarity threshold" rather than "force k clusters":

```python
from sentence_transformers.util import community_detection

communities = community_detection(embeddings, threshold=0.75, min_community_size=3)
```

## Paraphrase Mining

Use `paraphrase_mining` instead of brute-force all-pairs comparison for large lists:

```python
from sentence_transformers.util import paraphrase_mining

pairs = paraphrase_mining(model, sentences, top_k=10, max_pairs=1000)
for score, i, j in pairs[:10]:
    print(score, sentences[i], sentences[j])
```

Tune `query_chunk_size`, `corpus_chunk_size`, `top_k`, and `max_pairs` to trade memory, speed, and recall.

## Multimodal Embeddings

Install the relevant extra and verify model support:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")
print(model.modalities)
print(model.supports("image"))
```

Typical image inputs can be URLs, local paths, PIL images, or arrays. Multimodal dicts use modality keys such as `{"text": "...", "image": "..."}`. Chat-message input is model-specific and depends on the model's processor/chat template.

## Offline Or Local Models

Use local paths and `local_files_only=True`:

```python
model = SentenceTransformer("models/local-embedding-model", local_files_only=True)
```

Do not set `trust_remote_code=True` for arbitrary model repositories. Use it only when required and trusted.
