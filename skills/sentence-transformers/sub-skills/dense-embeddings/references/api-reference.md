# Dense Embedding API Reference

Read this for verified public signatures and parameters when writing dense embedding or semantic search code.

## `SentenceTransformer`

Constructor:

```python
SentenceTransformer(
    model_name_or_path: str | None = None,
    *,
    modules: list[nn.Module] | None = None,
    device: str | None = None,
    prompts: dict[str, str] | None = None,
    default_prompt_name: str | None = None,
    cache_folder: str | None = None,
    trust_remote_code: bool = False,
    revision: str | None = None,
    local_files_only: bool = False,
    token: bool | str | None = None,
    model_kwargs: dict[str, Any] | None = None,
    processor_kwargs: dict[str, Any] | None = None,
    config_kwargs: dict[str, Any] | None = None,
    backend: Literal["torch", "onnx", "openvino"] = "torch",
    similarity_fn_name: Literal["cosine", "dot", "euclidean", "manhattan"] | SimilarityFunction | None = None,
    truncate_dim: int | None = None,
)
```

Encoding:

```python
model.encode(
    inputs,
    prompt_name: str | None = None,
    prompt: str | None = None,
    batch_size: int = 32,
    show_progress_bar: bool | None = None,
    output_value: Literal["sentence_embedding", "token_embeddings"] | None = "sentence_embedding",
    precision: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32",
    convert_to_numpy: bool = True,
    convert_to_tensor: bool = False,
    device: str | list[str | torch.device] | None = None,
    normalize_embeddings: bool = False,
    truncate_dim: int | None = None,
    pool: dict[Literal["input", "output", "processes"], Any] | None = None,
    chunk_size: int | None = None,
    **kwargs,
)
```

`encode_query(...)` and `encode_document(...)` accept the same arguments. They differ from `encode` by applying query/document prompts when present and by setting the task for Router-based models.

Similarity:

```python
model.similarity(embeddings_a, embeddings_b)
model.similarity_pairwise(embeddings_a, embeddings_b)
```

`model.similarity` returns a matrix of all pair scores. `similarity_pairwise` returns pairwise scores for aligned inputs.

Saving/publishing:

```python
model.save_pretrained(path, model_name=None, create_model_card=True, train_datasets=None, safe_serialization=True)
model.push_to_hub(repo_id, token=None, private=None, safe_serialization=True, commit_message=None, exist_ok=False, create_pr=False)
```

## Dense Utilities

Exact search:

```python
semantic_search(
    query_embeddings,
    corpus_embeddings,
    query_chunk_size: int = 100,
    corpus_chunk_size: int = 500000,
    top_k: int = 10,
    score_function=cos_sim,
)
```

The return shape is `list[list[{"corpus_id": int, "score": float}]]`, one hit list per query.

Similarity functions:

```python
cos_sim(a, b) -> torch.Tensor
dot_score(a, b) -> torch.Tensor
```

Paraphrase mining:

```python
paraphrase_mining(
    model,
    sentences: list[str],
    show_progress_bar=False,
    batch_size=32,
    query_chunk_size=5000,
    corpus_chunk_size=100000,
    max_pairs=500000,
    top_k=100,
    score_function=cos_sim,
    truncate_dim=None,
    prompt_name=None,
    prompt=None,
)
```

Community detection:

```python
community_detection(
    embeddings,
    threshold: float = 0.75,
    min_community_size: int = 10,
    batch_size: int = 1024,
    show_progress_bar: bool = False,
)
```

Matryoshka truncation helper:

```python
truncate_embeddings(embeddings, truncate_dim)
```

Output embedding quantization helper:

```python
quantize_embeddings(
    embeddings,
    precision: Literal["float32", "int8", "uint8", "binary", "ubinary"],
    ranges=None,
    calibration_embeddings=None,
)
```

## Parameter Guidance

- `prompt_name` selects a stored prompt, while `prompt` passes a literal prompt string.
- `normalize_embeddings=True` is common for cosine/dot retrieval and ANN indexes.
- `precision` quantizes output embeddings during encoding. Validate recall before using compressed vectors in production.
- `truncate_dim` is useful for Matryoshka models; do not arbitrarily truncate non-Matryoshka embeddings without measuring quality.
- `pool` and multi-device `device` support multi-process encoding. Use only when simple batching is insufficient.
- `local_files_only=True` avoids network downloads when deploying cached/local models.
