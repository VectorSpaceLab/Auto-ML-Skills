# SparseEncoder API Reference

Read this for verified sparse embedding signatures and helper behavior.

## Constructor

```python
SparseEncoder(
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
    similarity_fn_name: str | SimilarityFunction | None = None,
    max_active_dims: int | None = None,
)
```

## Encoding

```python
model.encode(
    inputs,
    prompt_name: str | None = None,
    prompt: str | None = None,
    batch_size: int = 32,
    show_progress_bar: bool | None = None,
    convert_to_tensor: bool = True,
    convert_to_sparse_tensor: bool = True,
    save_to_cpu: bool = False,
    device: str | torch.device | list[str | torch.device] | None = None,
    max_active_dims: int | None = None,
    pool: dict[Literal["input", "output", "processes"], Any] | None = None,
    chunk_size: int | None = None,
    **kwargs,
)
```

`encode_query(...)` and `encode_document(...)` accept the same arguments and apply query/document prompts/tasks when available.

## Sparse Helpers

```python
SparseEncoder.sparsity(embeddings) -> dict[str, float]
```

Returns `active_dims` and `sparsity_ratio`.

```python
SparseEncoder.intersection(embeddings_1, embeddings_2) -> torch.Tensor
```

Computes elementwise intersection for shared active dimensions.

```python
model.decode(sparse_embedding, top_k=10)
```

Returns top active tokens and weights for interpretability.

## Search

`sentence_transformers.util.semantic_search` accepts sparse tensors and can use `score_function=model.similarity`.

```python
semantic_search(query_embeddings, corpus_embeddings, top_k=10, score_function=model.similarity)
```

For vector databases/search engines, check:

```python
from sentence_transformers.sparse_encoder.search_engines import (
    semantic_search_qdrant,
    semantic_search_opensearch,
)
```

These helpers require the corresponding client libraries and services.

## Parameter Guidance

- `max_active_dims` can cap active dimensions for efficiency; validate retrieval quality when changing it.
- `save_to_cpu=True` can help reduce GPU memory pressure after encoding.
- `convert_to_sparse_tensor=False` may be useful for libraries that cannot consume torch sparse tensors, but increases memory.
- Dot-product-style similarity is common for sparse models; use `model.similarity` unless a model or index requires another scoring function.
