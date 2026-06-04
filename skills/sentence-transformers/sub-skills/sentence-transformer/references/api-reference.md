# SentenceTransformer API Reference

Read this for verified public API signatures and parameter behavior that future agents commonly need when writing embedding, similarity, retrieval, save, and Hub-push code.

## Constructor

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
    model_card_data: SentenceTransformerModelCardData | None = None,
    backend: Literal["torch", "onnx", "openvino"] = "torch",
    similarity_fn_name: Literal["cosine", "dot", "euclidean", "manhattan"] | SimilarityFunction | None = None,
    truncate_dim: int | None = None,
)
```

Important parameters:

- `model_name_or_path`: Hugging Face model id, local model directory, or base Transformers checkpoint.
- `modules`: manual module chain, used for custom models.
- `device`: explicit device such as `"cuda"`, `"mps"`, or `"cpu"`.
- `prompts` and `default_prompt_name`: prompt templates used by `encode`.
- `trust_remote_code`: enable only for trusted model repositories.
- `backend`: choose `"torch"`, `"onnx"`, or `"openvino"`.
- `similarity_fn_name`: controls `model.similarity` and `model.similarity_pairwise`.
- `truncate_dim`: truncate output embeddings, useful for Matryoshka-compatible models.

## Encoding

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
    pool: dict | None = None,
    chunk_size: int | None = None,
    **kwargs,
)
```

`encode_query` and `encode_document` have the same signature as `encode`. Prefer them for retrieval:

- `encode_query` uses the model's `"query"` prompt if available and sets task `"query"`.
- `encode_document` uses a `"document"`, `"passage"`, or `"corpus"` prompt if available and sets task `"document"`.

Common return behavior:

- Default `convert_to_numpy=True` returns a NumPy array for sentence embeddings.
- `convert_to_tensor=True` returns a torch tensor.
- `output_value="token_embeddings"` returns token-level embeddings.
- `precision` can quantize output embeddings to `int8`, `uint8`, `binary`, or `ubinary`.
- `normalize_embeddings=True` L2-normalizes dense embeddings, commonly used with dot-product search.

## Similarity

`model.similarity` and `model.similarity_pairwise` are properties that return callables configured by `model.similarity_fn_name`.

Supported similarity functions include:

- `cosine`
- `dot`
- `euclidean`
- `manhattan`

Utility functions:

```python
from sentence_transformers.util import (
    cos_sim,
    dot_score,
    euclidean_sim,
    manhattan_sim,
    pairwise_cos_sim,
    pairwise_dot_score,
)
```

## Retrieval Utilities

```python
semantic_search(
    query_embeddings,
    corpus_embeddings,
    query_chunk_size: int = 100,
    corpus_chunk_size: int = 500000,
    top_k: int = 10,
    score_function=cos_sim,
) -> list[list[dict[str, int | float]]]
```

Each result contains `corpus_id` and `score`.

```python
paraphrase_mining(
    model,
    sentences: list[str],
    show_progress_bar: bool = False,
    batch_size: int = 32,
    query_chunk_size: int = 5000,
    corpus_chunk_size: int = 100000,
    max_pairs: int = 500000,
    top_k: int = 100,
    score_function=cos_sim,
    truncate_dim: int | None = None,
    prompt_name: str | None = None,
    prompt: str | None = None,
) -> list[list[float | int]]
```

`community_detection(embeddings, threshold=0.75, min_community_size=10, batch_size=1024)` clusters embeddings by similarity threshold.

## Multi-Process Embedding

```python
pool = model.start_multi_process_pool(target_devices: list[str] | None = None)
embeddings = model.encode_multi_process(
    sentences,
    pool,
    prompt_name=None,
    prompt=None,
    batch_size=32,
    chunk_size=None,
    show_progress_bar=None,
    precision="float32",
    normalize_embeddings=False,
    truncate_dim=None,
)
model.stop_multi_process_pool(pool)
```

Use this for large offline embedding jobs across multiple devices. Prefer ordinary `encode` for small workloads.

## Save And Hub Push

```python
model.save_pretrained(
    path: str,
    model_name: str | None = None,
    create_model_card: bool = True,
    train_datasets: list[str] | None = None,
    safe_serialization: bool = True,
)
```

```python
model.push_to_hub(
    repo_id: str,
    token: str | None = None,
    private: bool | None = None,
    safe_serialization: bool = True,
    commit_message: str | None = None,
    local_model_path: str | None = None,
    exist_ok: bool = False,
    replace_model_card: bool = False,
    train_datasets: list[str] | None = None,
    revision: str | None = None,
    create_pr: bool = False,
) -> str
```

Saved models contain `modules.json`, `config_sentence_transformers.json`, module folders, tokenizer/config files, weights, and often a generated model card.
