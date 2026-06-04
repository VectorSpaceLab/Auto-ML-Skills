# Training Data Formats

Read this before selecting a loss. The dataset column pattern determines valid losses, collators, and evaluator setup.

## Loading Data

Use Hugging Face Datasets:

```python
from datasets import load_dataset

dataset = load_dataset("csv", data_files="train.csv", split="train")
dataset = load_dataset("json", data_files="train.jsonl", split="train")
dataset = load_dataset("sentence-transformers/all-nli", "pair", split="train")
```

Local formats commonly supported by `datasets` include CSV, JSON/JSONL, Parquet, Arrow, text, and SQL-backed workflows.

## Dense Embedding Formats

`(anchor, positive)` with no labels:

```text
anchor | positive
```

Use in-batch negative losses such as `MultipleNegativesRankingLoss` or `CachedMultipleNegativesRankingLoss`.

`(anchor, positive, negative)`:

```text
anchor | positive | negative
```

Use triplet or in-batch negative losses depending on objective.

`(input_A, input_B, score)`:

```text
sentence1 | sentence2 | score
```

Use similarity regression/ranking losses such as `CoSENTLoss`, `AnglELoss`, or `CosineSimilarityLoss`.

`single input + class`:

```text
text | label
```

Use triplet-style batch losses that use labels to form positives/negatives.

Teacher distillation:

```text
text | teacher_embedding
query | positive | negative | teacher_scores
```

Use `MSELoss`, `EmbedDistillLoss`, `MarginMSELoss`, or `DistillKLDivLoss` depending on label shape.

## Cross Encoder Formats

Binary or regression pair scoring:

```text
query | document | label
```

Use `BinaryCrossEntropyLoss`, `MSELoss`, or `MarginMSELoss` depending on label semantics.

Multi-class pair classification:

```text
premise | hypothesis | label
```

Use `CrossEntropyLoss`; set `num_labels` to class count.

Listwise reranking:

```text
query | documents | scores
```

Where `documents` and `scores` are lists. Use `LambdaLoss`, `ListNetLoss`, `ListMLELoss`, `PListMLELoss`, `RankNetLoss`, or `ADRMSELoss`.

In-batch reranker training:

```text
anchor | positive
anchor | positive | negative
```

Use Cross Encoder multiple-negatives losses, often after hard-negative mining.

## Sparse Encoder Formats

Sparse formats mirror dense embedding formats:

```text
anchor | positive
anchor | positive | negative
sentence1 | sentence2 | score
query | positive | negative_1 ... | teacher_scores
```

For SPLADE models, wrap the main sparse loss in `SpladeLoss` or `CachedSpladeLoss` to regularize sparsity.

## Column Naming

Column names can vary, but names should make role and label meaning obvious. Common names:

- `anchor`, `positive`, `negative`
- `query`, `document`, `documents`
- `sentence1`, `sentence2`, `score`
- `premise`, `hypothesis`, `label`
- `text`, `label`

When a model uses `Router`, set `router_mapping` in training arguments:

```python
args = SentenceTransformerTrainingArguments(
    output_dir="...",
    router_mapping={"question": "query", "answer": "document"},
)
```

## Validation Checklist

Before calling `trainer.train()`:

- Print `dataset.column_names`.
- Inspect a few rows.
- Confirm labels are floats for regression and ints/classes for classification.
- Confirm listwise columns are lists with matching lengths.
- Confirm chosen loss supports that exact pattern.
- Confirm evaluator uses the same semantic target as the user cares about.
