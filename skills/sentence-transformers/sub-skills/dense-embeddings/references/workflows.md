# Dense Embedding Workflows

Read this for task recipes around `SentenceTransformer`.

## Semantic Textual Similarity

Use this when all texts are comparable units such as sentences, question pairs, titles, or abstracts.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = ["A man is eating pasta.", "A person eats food.", "The sky is blue."]
embeddings = model.encode(texts, convert_to_tensor=True)
scores = model.similarity(embeddings, embeddings)
```

Use `encode`, not query/document methods, unless the model documentation says to use prompts for the task.

## Asymmetric Semantic Search

Use for short queries against longer documents/passages.

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
corpus_embeddings = model.encode_document(corpus, convert_to_tensor=True, normalize_embeddings=True)
query_embeddings = model.encode_query(queries, convert_to_tensor=True, normalize_embeddings=True)
hits = semantic_search(query_embeddings, corpus_embeddings, top_k=10)
```

For repeated use, compute `corpus_embeddings` once and persist it with the corpus text, model id, model revision, prompt settings, normalization choice, and embedding dtype.

## Symmetric Search

Use for similar questions, duplicate detection, or similar papers where queries and corpus entries have the same shape.

```python
embeddings = model.encode(all_texts, convert_to_tensor=True, normalize_embeddings=True)
```

When searching one subset against another, either use `semantic_search` or `model.similarity`.

## Retrieve And Rerank

Dense embeddings should retrieve candidates efficiently; `CrossEncoder` reranks them.

```python
from sentence_transformers import CrossEncoder, SentenceTransformer
from sentence_transformers.util import semantic_search

retriever = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

doc_emb = retriever.encode_document(corpus, convert_to_tensor=True, normalize_embeddings=True)
query_emb = retriever.encode_query([query], convert_to_tensor=True, normalize_embeddings=True)
candidate_hits = semantic_search(query_emb, doc_emb, top_k=50)[0]
candidate_docs = [corpus[hit["corpus_id"]] for hit in candidate_hits]
reranked = reranker.rank(query, candidate_docs, return_documents=True, top_k=10)
```

Keep original corpus ids when mapping reranked candidate ids back to the full corpus.

## Paraphrase Mining

Use `paraphrase_mining` for finding high-similarity pairs within one list.

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import paraphrase_mining

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
pairs = paraphrase_mining(model, sentences, top_k=20)
for score, i, j in pairs[:20]:
    print(score, sentences[i], sentences[j])
```

Tune `top_k`, `max_pairs`, and chunk sizes for large lists.

## Clustering And Communities

Use embeddings with scikit-learn clustering or `community_detection`.

```python
from sentence_transformers.util import community_detection

embeddings = model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)
communities = community_detection(embeddings, threshold=0.75, min_community_size=5)
```

The threshold is task/model dependent; inspect sampled communities and adjust.

## Multimodal Embeddings

Use only models that declare support for the desired modality.

```python
model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")
print(model.modalities)
print(model.supports("image"))
image_embeddings = model.encode(["path/to/image.jpg"])
text_embeddings = model.encode(["a photo of a car"])
scores = model.similarity(text_embeddings, image_embeddings)
```

Install `sentence-transformers[image]`, `[audio]`, or `[video]` as needed. Avoid URL inputs in smoke tests unless network use is explicitly acceptable.

## Large-Scale Search

Exact `semantic_search` is convenient up to about 1M corpus entries, depending on embedding dimension and hardware. For larger or lower-latency systems:

- Normalize embeddings if the index uses inner product for cosine search.
- Store corpus ids and metadata separately from vectors.
- Use FAISS/hnswlib/Annoy for local ANN.
- Use Elasticsearch, OpenSearch, Qdrant, Milvus, Weaviate, or similar for services.
- Validate recall with a held-out query set before switching from exact search to ANN.
