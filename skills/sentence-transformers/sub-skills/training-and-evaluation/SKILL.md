---
name: training-and-evaluation
description: "Use for fine-tuning SentenceTransformer, CrossEncoder, and SparseEncoder models with datasets, losses, trainers, training arguments, evaluators, hard-negative mining, distributed training, and model cards."
disable-model-invocation: true
---

# Training And Evaluation

Use this sub-skill when the task involves fine-tuning or evaluating embedding models, rerankers, or sparse encoders with Sentence Transformers.

Training uses Hugging Face `datasets.Dataset` objects, model-specific trainer classes, model-specific training arguments, losses matched to dataset columns, and optional evaluators.

## When To Use

Use this sub-skill when the user asks to:

- fine-tune a dense embedding model, Cross Encoder reranker/classifier, or Sparse Encoder;
- choose a loss from dataset shape and labels;
- prepare local CSV/JSON/Parquet/Arrow/SQL or Hub datasets;
- use `SentenceTransformerTrainer`, `CrossEncoderTrainer`, or `SparseEncoderTrainer`;
- configure `SentenceTransformerTrainingArguments`, `CrossEncoderTrainingArguments`, or `SparseEncoderTrainingArguments`;
- evaluate with STS, IR, reranking, triplet, classification, NanoBEIR, or sparse evaluators;
- mine hard negatives from positive pairs;
- run distributed training or resume/push model artifacts.

Use model-family sub-skills first for inference-only tasks.

## Read These Files

Read [references/training-api.md](references/training-api.md) for verified trainer and training-argument signatures, shared arguments, and model-specific options.

Read [references/data-formats.md](references/data-formats.md) before choosing a loss. Most training failures come from mismatched dataset columns.

Read [references/loss-selection.md](references/loss-selection.md) for dense, Cross Encoder, and sparse loss choices by input/label pattern.

Read [references/evaluation.md](references/evaluation.md) for evaluator families and when to use each evaluator.

Read [references/hard-negatives-and-distributed.md](references/hard-negatives-and-distributed.md) for `mine_hard_negatives`, distributed training, and large-batch patterns.

Read [references/troubleshooting.md](references/troubleshooting.md) when collators fail, columns are dropped, losses get the wrong shape, sparse vectors are not sparse, or training quality is poor.

Run or adapt [scripts/training_import_check.py](scripts/training_import_check.py) to verify trainer, loss, evaluator, `datasets`, and `accelerate` availability without starting training.

Run or adapt [scripts/minimal_dense_training_template.py](scripts/minimal_dense_training_template.py) as a small dense training skeleton. It is intentionally tiny and should be adapted before real training.

## Short Workflow

1. Install training dependencies with `pip install -U "sentence-transformers[train]"`.
2. Identify model family: dense `SentenceTransformer`, `CrossEncoder`, or `SparseEncoder`.
3. Inspect dataset columns and label semantics.
4. Choose a loss that matches columns and model output shape.
5. Add an evaluator that matches the target metric, not just the training loss.
6. Configure training arguments with output directory, batch size, epochs/steps, eval/save cadence, and Hub options.
7. Instantiate the model-specific trainer and call `trainer.train()`.
8. Save locally with `save_pretrained` or push with `push_to_hub` / `push_to_hub=True`.

## Minimal Dense Training Skeleton

```python
from datasets import Dataset
from sentence_transformers import SentenceTransformer, SentenceTransformerTrainer, SentenceTransformerTrainingArguments
from sentence_transformers.sentence_transformer import losses

train_dataset = Dataset.from_dict({
    "anchor": ["What is Python?", "What is Mars?"],
    "positive": ["Python is a programming language.", "Mars is the Red Planet."],
})

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
loss = losses.MultipleNegativesRankingLoss(model)
args = SentenceTransformerTrainingArguments(
    output_dir="models/example-embedding",
    num_train_epochs=1,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
)
trainer = SentenceTransformerTrainer(model=model, args=args, train_dataset=train_dataset, loss=loss)
trainer.train()
model.save_pretrained("models/example-embedding")
```

## Minimal Cross Encoder Training Shape

```python
from datasets import Dataset
from sentence_transformers import CrossEncoder, CrossEncoderTrainer, CrossEncoderTrainingArguments
from sentence_transformers.cross_encoder import losses

train_dataset = Dataset.from_dict({
    "query": ["What is Python?", "What is Python?"],
    "document": ["Python is a programming language.", "Mars is a planet."],
    "label": [1.0, 0.0],
})

model = CrossEncoder("google-bert/bert-base-uncased", num_labels=1)
loss = losses.BinaryCrossEntropyLoss(model)
args = CrossEncoderTrainingArguments(output_dir="models/example-reranker", per_device_train_batch_size=8)
trainer = CrossEncoderTrainer(model=model, args=args, train_dataset=train_dataset, loss=loss)
```

## Minimal Sparse Training Shape

For SPLADE, wrap the main sparse loss:

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder import losses

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
main_loss = losses.SparseMultipleNegativesRankingLoss(model)
loss = losses.SpladeLoss(model, loss=main_loss)
```

Use `SparseEncoderTrainer` and `SparseEncoderTrainingArguments` as the trainer/arguments pair.

## Key Rule

Do not choose a loss by model family alone. Choose it from dataset columns, labels, intended metric, and model output shape.
