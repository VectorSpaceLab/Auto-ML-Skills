# Inference Workflows

Use these patterns as starting points when writing FlagEmbedding inference code. The snippets assume CPU-safe defaults; switch devices and precision only when the target machine supports them.

## Basic Dense Embeddings

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "BAAI/bge-base-en-v1.5",
    normalize_embeddings=True,
    use_fp16=False,
    devices="cpu",
)

sentences = ["I love NLP", "I love text retrieval"]
embeddings = model.encode(sentences, batch_size=32, max_length=512)
print(embeddings.shape)
```

Use this for clustering, semantic search indexing, or plain sentence similarity. With normalized embeddings, `embeddings_a @ embeddings_b.T` is the usual similarity calculation.

## Query And Corpus Retrieval

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "BAAI/bge-large-en-v1.5",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ",
    query_instruction_format="{}{}",
    normalize_embeddings=True,
    use_fp16=False,
    devices="cpu",
)

queries = ["how do dense retrievers work?"]
corpus = [
    "Dense retrievers encode text into vectors and compare vector similarity.",
    "Cross-encoders rerank query-document pairs directly.",
]

query_vectors = model.encode_queries(queries, batch_size=16, max_length=128)
passage_vectors = model.encode_corpus(corpus, batch_size=16, max_length=512)
scores = query_vectors @ passage_vectors.T
ranked = sorted(zip(corpus, scores[0]), key=lambda item: item[1], reverse=True)
```

Use `encode_queries()` when a retrieval instruction is configured; it formats only the query side. Use `encode_corpus()` for passages so query instructions are not accidentally prepended to documents.

## Custom Or Renamed Embedder Checkpoint

Auto mapping uses the basename of `model_name_or_path`; if a local directory is named `checkpoint-1000`, it checks the parent basename. If that name is not mapped, pass `model_class` and architecture-specific options explicitly.

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "./my-local-embedder",
    model_class="encoder-only-base",
    pooling_method="cls",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ",
    query_instruction_format="{}{}",
    normalize_embeddings=True,
    use_fp16=False,
    devices="cpu",
)
```

Common embedder `model_class` values:

- `encoder-only-base`: `FlagModel` style dense encoder.
- `encoder-only-m3`: `BGEM3FlagModel` style BGE-M3 output dictionary.
- `decoder-only-base`: `FlagLLMModel` style last-token LLM embedder.
- `decoder-only-icl`: `FlagICLModel` style in-context-learning embedder.
- `decoder-only-pseudo_moe`: `FlagPseudoMoEModel` style pseudo-MoE embedder.

## BGE-M3 Dense And Sparse Scoring

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel(
    "BAAI/bge-m3",
    normalize_embeddings=True,
    use_fp16=False,
    devices="cpu",
)

queries = ["what is vector search?"]
passages = [
    "Vector search compares dense embeddings.",
    "Sparse retrieval matches weighted lexical terms.",
]

q_out = model.encode_queries(
    queries,
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)
p_out = model.encode_corpus(
    passages,
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)

dense_scores = q_out["dense_vecs"] @ p_out["dense_vecs"].T
sparse_scores = model.compute_lexical_matching_score(
    q_out["lexical_weights"],
    p_out["lexical_weights"],
)
```

BGE-M3 outputs are dictionaries. Do not pass the entire output object into code that expects a NumPy matrix; select `dense_vecs`, `lexical_weights`, or `colbert_vecs` intentionally.

## BGE-M3 ColBERT Vectors

```python
outputs = model.encode(
    ["multi-vector example"],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=True,
)
colbert_vectors = outputs["colbert_vecs"]
```

`colbert_vecs` is a list-like collection of token-level vectors. It is useful for late-interaction retrieval, but it is larger than dense embeddings and may require downstream code that understands multi-vector scoring.

## Basic Reranking

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "BAAI/bge-reranker-base",
    use_fp16=False,
    devices="cpu",
    query_max_length=256,
    max_length=512,
)

pairs = [
    ["what is panda?", "hi"],
    ["what is panda?", "The giant panda is a bear species endemic to China."],
]
raw_scores = reranker.compute_score(pairs)
normalized_scores = reranker.compute_score(pairs, normalize=True)
```

Use rerankers after a first-stage retriever has selected a small candidate set. Raw scores are model logits; `normalize=True` applies sigmoid normalization.

## Custom Or Renamed Reranker Checkpoint

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "./my-local-reranker",
    model_class="encoder-only-base",
    use_fp16=False,
    devices="cpu",
    query_max_length=256,
    max_length=512,
)
score = reranker.compute_score(["query", "candidate passage"])
```

Common reranker `model_class` values:

- `encoder-only-base`: `FlagReranker` style sequence-classification reranker.
- `decoder-only-base`: `FlagLLMReranker` style decoder-only reranker.
- `decoder-only-layerwise`: `LayerWiseFlagLLMReranker` style layer-selective reranker.
- `decoder-only-lightweight`: `LightWeightFlagLLMReranker` style compressed/lightweight reranker.

## Layerwise Reranker

```python
from FlagEmbedding import LayerWiseFlagLLMReranker

reranker = LayerWiseFlagLLMReranker(
    "BAAI/bge-reranker-v2-minicpm-layerwise",
    use_fp16=False,
    devices="cpu",
    query_max_length=256,
    max_length=512,
)
score = reranker.compute_score(["query", "passage"], cutoff_layers=[28])
```

`cutoff_layers` selects which intermediate layer output is used. Lower layers can reduce cost but may change ranking quality.

## Lightweight Reranker

```python
from FlagEmbedding import LightWeightFlagLLMReranker

reranker = LightWeightFlagLLMReranker(
    "BAAI/bge-reranker-v2.5-gemma2-lightweight",
    use_fp16=False,
    devices="cpu",
    query_max_length=256,
    max_length=512,
)
score = reranker.compute_score(
    ["query", "passage"],
    cutoff_layers=[28],
    compress_ratio=2,
    compress_layers=[24, 40],
)
```

Use `compress_ratio` and `compress_layers` only for lightweight rerankers. Passing these kwargs to ordinary rerankers may fail or be ignored depending on implementation.

## Instruction Formatting

```python
model = FlagAutoModel.from_finetuned(
    "BAAI/bge-multilingual-gemma2",
    model_class="decoder-only-base",
    pooling_method="last_token",
    query_instruction_for_retrieval="Given a question, retrieve passages that answer it.",
    query_instruction_format="<instruct>{}\n<query>{}",
    use_fp16=False,
    devices="cpu",
)
```

Instruction format strings must have two `{}` slots: the instruction and the original text. Literal `"\\n"` sequences are converted into newlines by the base classes.

## Batch And Length Controls

- Lower `batch_size` when GPU memory is exhausted or CPU inference is slow and swapping.
- Lower `query_max_length` for short search queries, often `128` or `256`.
- Keep `passage_max_length` or `max_length` large enough for candidate passages, commonly `512`.
- Use per-call overrides, such as `encode_queries(..., batch_size=16, max_length=128)`, when one workflow has mixed sizes.
- Use `truncate_dim` at model construction for compatible embeddings when downstream indexes require smaller vectors.

## Device And Precision Controls

- CPU-safe default: `devices="cpu"`, `use_fp16=False`, `use_bf16=False`.
- CUDA single GPU: `devices="cuda:0"`, often with `use_fp16=True` if supported.
- CUDA multi-GPU: `devices=["cuda:0", "cuda:1"]`; this triggers multi-process behavior for list inputs.
- Integer devices, such as `devices=0`, become `"cuda:0"` unless MUSA is available.
- Avoid `use_fp16=True` on CPU; several concrete classes force FP16 off for CPU, but explicit false is clearer.
