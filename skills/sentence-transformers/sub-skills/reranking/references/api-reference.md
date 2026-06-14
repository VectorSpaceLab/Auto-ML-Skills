# CrossEncoder API Reference

Read this for verified `CrossEncoder` signatures and parameter behavior.

## Constructor

```python
CrossEncoder(
    model_name_or_path: str | None = None,
    *,
    modules: list[nn.Module] | OrderedDict[str, nn.Module] | None = None,
    device: str | None = None,
    prompts: dict[str, str] | None = None,
    default_prompt_name: str | None = None,
    cache_folder: str | None = None,
    trust_remote_code: bool = False,
    revision: str | None = None,
    local_files_only: bool = False,
    token: bool | str | None = None,
    model_kwargs: dict | None = None,
    processor_kwargs: dict | None = None,
    config_kwargs: dict | None = None,
    backend: Literal["torch", "onnx", "openvino"] = "torch",
    num_labels: int | None = None,
    max_length: int | None = None,
    activation_fn: Callable | None = None,
)
```

`num_labels`, `max_length`, `activation_fn`, and `device` should be passed as keyword arguments.

## Predict

```python
model.predict(
    inputs,
    prompt_name: str | None = None,
    prompt: str | None = None,
    batch_size: int = 32,
    show_progress_bar: bool | None = None,
    activation_fn: Callable | None = None,
    apply_softmax: bool | None = False,
    convert_to_numpy: bool = True,
    convert_to_tensor: bool = False,
    device: str | list[str | torch.device] | None = None,
    pool: dict[Literal["input", "output", "processes"], Any] | None = None,
    chunk_size: int | None = None,
    **kwargs,
)
```

`inputs` is one pair or a list of pairs. Pair elements can be strings or supported multimodal inputs depending on model capabilities.

## Rank

```python
model.rank(
    query,
    documents: list,
    top_k: int | None = None,
    return_documents: bool = False,
    prompt_name: str | None = None,
    prompt: str | None = None,
    batch_size: int = 32,
    show_progress_bar: bool | None = None,
    activation_fn: Callable | None = None,
    apply_softmax=False,
    convert_to_numpy: bool = True,
    convert_to_tensor: bool = False,
    device: str | list[str | torch.device] | None = None,
    pool=None,
    chunk_size: int | None = None,
)
```

Return shape:

```python
[
    {"corpus_id": 0, "score": 8.61},
    {"corpus_id": 2, "score": 6.35},
]
```

With `return_documents=True`, rows include `"text"` containing the corresponding candidate document.

## Save And Publish

```python
model.save_pretrained(path, model_name=None, create_model_card=True, train_datasets=None, safe_serialization=True)
model.push_to_hub(repo_id, token=None, private=None, safe_serialization=True, commit_message=None, exist_ok=False, create_pr=False)
```

## Multimodal Support

Check model capabilities:

```python
print(model.modalities)
print(model.supports("image"))
print(model.supports(("text", "image")))
```

Each side of a pair can be a supported modality. Vision-language rerankers may accept text queries and image or text documents.

## Score Handling

- `activation_fn` on the constructor sets the model default.
- `activation_fn` passed to `predict` or `rank` applies to that call and does not permanently modify the instance.
- `apply_softmax=True` is relevant for multiclass logits.
- MS MARCO reranking models generally produce logits; use sigmoid only when calibrated probabilities are needed.
