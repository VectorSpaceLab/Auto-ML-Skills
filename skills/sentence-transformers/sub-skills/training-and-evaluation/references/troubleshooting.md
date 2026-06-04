# Training Troubleshooting

## Trainer Fails On Columns

Print columns and sample rows:

```python
print(train_dataset.column_names)
print(train_dataset[0])
```

Compare them with the selected loss. Most collator and forward-shape errors are dataset/loss mismatches.

## Loss Receives Wrong Label Shape

Check whether labels are:

- absent for in-batch-negative losses;
- scalar floats for regression/binary relevance;
- integer class ids for cross entropy;
- lists of scores for listwise losses;
- vectors/tensors for embedding distillation.

Convert column types before training if needed.

## `remove_unused_columns` Drops Needed Columns

Training arguments default to `remove_unused_columns=True`. If custom losses or collators need nonstandard columns and they disappear, set `remove_unused_columns=False` or adapt column names and collator logic.

## Sparse Training Is Not Sparse

For SPLADE, wrap the main sparse loss with `SpladeLoss` or `CachedSpladeLoss`. Monitor `SparseEncoder.sparsity(...)` on validation embeddings.

## Cross Encoder Output Shape Wrong

Set `num_labels` correctly when loading from a generic checkpoint:

- `num_labels=1` for reranking/regression.
- `num_labels=N` for N-class classification.

Match loss and evaluator to `num_labels`.

## Retrieval Quality Does Not Improve

Check:

- model family matches task shape;
- loss matches dataset;
- negatives are hard but not false;
- evaluator measures the actual target metric;
- query/document prompts are applied;
- train/eval split avoids leakage.

## Training Is Slow Or OOM

Reduce batch size, use gradient accumulation, enable fp16/bf16 if hardware supports it, use cached losses where appropriate, reduce max sequence length, or use a smaller base model.

For large in-batch-negative training, prefer cached losses or distributed training over silently shrinking batch size until the objective weakens.

## Hub Push Or Model Card Problems

Confirm authentication, `hub_model_id`, and whether the repo exists or `exist_ok`/`push_to_hub` behavior is desired. For private models, set `hub_private_repo=True`.

If generated model cards include missing dataset metadata, pass `train_datasets` when saving or pushing.
