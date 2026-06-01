# Training API Reference

Read this for verified trainer constructor signatures and key training argument behavior.

## Trainer Classes

Dense embedding models:

```python
SentenceTransformerTrainer(
    model: SentenceTransformer | None = None,
    args: SentenceTransformerTrainingArguments | None = None,
    train_dataset=None,
    eval_dataset=None,
    loss=None,
    evaluator=None,
    data_collator=None,
    processing_class=None,
    model_init=None,
    compute_metrics=None,
    callbacks=None,
    optimizers=(None, None),
    optimizer_cls_and_kwargs=None,
    preprocess_logits_for_metrics=None,
)
```

Cross Encoder models:

```python
CrossEncoderTrainer(
    model: CrossEncoder | None = None,
    args: CrossEncoderTrainingArguments | None = None,
    train_dataset=None,
    eval_dataset=None,
    loss=None,
    evaluator=None,
    data_collator=None,
    processing_class=None,
    model_init=None,
    compute_metrics=None,
    callbacks=None,
    optimizers=(None, None),
    optimizer_cls_and_kwargs=None,
    preprocess_logits_for_metrics=None,
)
```

Sparse Encoder models:

```python
SparseEncoderTrainer(
    model: SparseEncoder | None = None,
    args: SparseEncoderTrainingArguments | None = None,
    train_dataset=None,
    eval_dataset=None,
    loss=None,
    evaluator=None,
    data_collator=None,
    processing_class=None,
    model_init=None,
    compute_metrics=None,
    callbacks=None,
    optimizers=(None, None),
    optimizer_cls_and_kwargs=None,
    preprocess_logits_for_metrics=None,
)
```

`train_dataset` and `eval_dataset` can be `datasets.Dataset`, `DatasetDict`, `IterableDataset`, or dicts of datasets for multi-dataset training. `loss` can be one loss, a dict of losses, a callable that receives the model, or a dict of such callables.

## Training Arguments

The three argument classes share a large Hugging Face Trainer-style surface:

- `output_dir`
- `per_device_train_batch_size`
- `per_device_eval_batch_size`
- `num_train_epochs`
- `max_steps`
- `learning_rate`
- `warmup_steps` / `warmup_ratio`
- `lr_scheduler_type`
- `fp16`, `bf16`, `tf32`
- `gradient_accumulation_steps`
- `gradient_checkpointing`
- `eval_strategy`, `eval_steps`
- `save_strategy`, `save_steps`, `save_total_limit`
- `logging_steps`, `report_to`
- `push_to_hub`, `hub_model_id`, `hub_private_repo`, `hub_strategy`
- `load_best_model_at_end`, `metric_for_best_model`
- distributed options such as `ddp_*`, `fsdp`, and `deepspeed`

Sentence Transformers adds model-specific fields:

- `prompts`: one prompt or mapping of prompts applied to training columns.
- `batch_sampler`: default batch sampler strategy.
- `multi_dataset_batch_sampler`: strategy for multi-dataset training.
- `router_mapping`: maps dataset columns to router routes such as `"query"` or `"document"`.
- `learning_rate_mapping`: assign learning rates to module patterns.

## Dataset And Loss Mapping

When `train_dataset` is a `DatasetDict` or dict, pass a matching dict of losses if each subset has a different format.

```python
loss = {
    "retrieval": losses.MultipleNegativesRankingLoss(model),
    "sts": losses.CoSENTLoss(model),
}
```

Use `multi_dataset_batch_sampler` to control how batches are drawn across datasets.

## Model Cards And Logging

Training can generate model card metadata when models are saved. Install optional logging tools explicitly:

```bash
pip install trackio
pip install wandb
pip install codecarbon
```

Then set `report_to` in training arguments.

## Precision Guidance

For training, loading the model in fp32 is often safer if memory allows. You can still use `fp16=True` or `bf16=True` in training arguments for mixed precision. Loading all weights directly in reduced precision can round small updates to zero for some workflows.

## New Trainer Versus Legacy Fit

Prefer model-specific trainers for new work. Legacy `.fit(...)` methods exist for backward compatibility, especially on `CrossEncoder`, but trainers integrate better with datasets, callbacks, Hub push, and modern training arguments.
