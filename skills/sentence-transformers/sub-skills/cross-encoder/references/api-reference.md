# CrossEncoder API Reference

Read this when writing or reviewing pair-scoring, ranking, saving, or legacy `fit` code.

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
    model_card_data: CrossEncoderModelCardData | None = None,
    backend: Literal["torch", "onnx", "openvino"] = "torch",
    num_labels: int | None = None,
    max_length: int | None = None,
    activation_fn: Callable | None = None,
)
```

Important parameters:

- `num_labels=1`: reranking/regression-style score.
- `num_labels>1`: pair classification.
- `max_length`: truncation length for paired inputs.
- `activation_fn`: optional post-processing for logits, such as sigmoid.
- `backend`: `"torch"`, `"onnx"`, or `"openvino"`.

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
    pool: dict | None = None,
    chunk_size: int | None = None,
    **kwargs,
) -> list[torch.Tensor] | np.ndarray | torch.Tensor
```

`inputs` can be a single pair or a list of pairs. A pair is commonly a tuple/list of two texts, but multimodal models can accept supported modality objects or dictionaries.

Use `apply_softmax=True` for multi-class outputs when probabilities are required. Use `activation_fn` for custom activation, such as sigmoid for binary logits.

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
    pool: dict | None = None,
    chunk_size: int | None = None,
) -> list[dict[Literal["corpus_id", "score", "text"], int | float | str]]
```

Returned dictionaries include:

- `corpus_id`: original index in the `documents` list.
- `score`: model score.
- `text`: included when `return_documents=True`.

`top_k=None` returns all ranked documents.

## Legacy Fit

`CrossEncoder.fit(...)` exists for legacy dataloader training:

```python
model.fit(
    train_dataloader,
    evaluator=None,
    epochs=1,
    loss_fct=None,
    activation_fct=Identity(),
    scheduler="WarmupLinear",
    warmup_steps=10000,
    optimizer_class=torch.optim.AdamW,
    optimizer_params={"lr": 2e-5},
    weight_decay=0.01,
    evaluation_steps=0,
    output_path=None,
    save_best_model=True,
    max_grad_norm=1,
    use_amp=False,
    callback=None,
    show_progress_bar=True,
)
```

For new training code, prefer `CrossEncoderTrainer` and `CrossEncoderTrainingArguments` from the training sub-skill.

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

Saved CrossEncoder directories include `modules.json`, `config_sentence_transformers.json`, module files, tokenizer/config/weight files, and usually a model card.
