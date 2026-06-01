# SparseEncoder API Reference

Read this when writing sparse embedding, sparse search, interpretability, save, or Hub-push code.

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
    model_card_data: SparseEncoderModelCardData | None = None,
    backend: Literal["torch", "onnx", "openvino"] = "torch",
    similarity_fn_name: str | SimilarityFunction | None = None,
    max_active_dims: int | None = None,
)
```

Important parameters:

- `similarity_fn_name`: often `"dot"` for sparse retrieval.
- `max_active_dims`: limits active dimensions per embedding.
- `backend`: `"torch"`, `"onnx"`, or `"openvino"`.
- `model_kwargs`: pass model precision or backend-specific load options.

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
    pool: dict | None = None,
    chunk_size: int | None = None,
    **kwargs,
) -> list[Tensor] | Tensor
```

`encode_query` and `encode_document` have the same signature as `encode`. Prefer them for retrieval so prompts and router tasks are applied.

Common choices:

- `convert_to_sparse_tensor=True`: keep sparse tensors when possible.
- `save_to_cpu=True`: useful for large document-encoding jobs.
- `max_active_dims=N`: keep only top active dimensions to reduce index size.

## Similarity And Pairwise Inspection

`model.similarity` is a property that returns a callable. Sparse retrieval commonly uses dot product.

```python
hits = semantic_search(query_embeddings, corpus_embeddings, score_function=model.similarity)
```

`SparseEncoder.intersection(embeddings_1, embeddings_2)` returns pointwise overlap scores, useful for token-level match inspection.

## Sparsity

```python
SparseEncoder.sparsity(embeddings: torch.Tensor) -> dict[str, float]
```

Returned keys include summary metrics such as sparsity ratio and active dimensions. Use this after changing `max_active_dims`, regularization, or model choice.

## Decode

```python
model.decode(embeddings: torch.Tensor, top_k: int | None = None) -> list[tuple[str, float]] | list[list[tuple[str, float]]]
```

`decode` maps active dimensions back to tokenizer terms and scores. Use it for interpretability and debugging, not as a replacement for search.

## Save And Hub Push

```python
model.save_pretrained(path, model_name=None, create_model_card=True, train_datasets=None, safe_serialization=True)
```

```python
model.push_to_hub(
    repo_id,
    token=None,
    private=None,
    safe_serialization=True,
    commit_message=None,
    local_model_path=None,
    exist_ok=False,
    replace_model_card=False,
    train_datasets=None,
    revision=None,
    create_pr=False,
) -> str
```

Saved SparseEncoder models use the same module-based model directory pattern as SentenceTransformer models.

## Search Engine Helpers

The package includes sparse search-engine helper functions under `sentence_transformers.sparse_encoder.search_engines`. Use them as integration references for systems such as Qdrant, OpenSearch, Elasticsearch, Seismic, and SPLADE-style indexes. Install each external client separately.
