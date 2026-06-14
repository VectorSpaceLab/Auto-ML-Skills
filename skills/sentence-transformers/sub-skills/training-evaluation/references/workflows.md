# Training And Evaluation Workflows

Read this before writing or debugging training code.

## Step 1: Identify Task And Data Shape

Ask or infer:

- model family: dense `SentenceTransformer`, `CrossEncoder`, or `SparseEncoder`;
- data columns and labels;
- target metric: STS correlation, retrieval nDCG/MRR/Recall, pair classification accuracy/F1, reranking nDCG/MRR, sparse active dims plus ranking quality;
- base model and language/domain;
- hardware and time budget;
- whether Hub publishing is required.

## Dense Embedding Training

Pair retrieval example:

```python
from datasets import Dataset
from sentence_transformers import SentenceTransformer, SentenceTransformerTrainer, SentenceTransformerTrainingArguments
from sentence_transformers.sentence_transformer.losses import MultipleNegativesRankingLoss

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
train_dataset = Dataset.from_dict({"anchor": anchors, "positive": positives})
loss = MultipleNegativesRankingLoss(model)
args = SentenceTransformerTrainingArguments(
    output_dir="models/dense-run",
    per_device_train_batch_size=32,
    learning_rate=2e-5,
    num_train_epochs=1,
    warmup_steps=0.1,
    report_to="none",
)
trainer = SentenceTransformerTrainer(model=model, args=args, train_dataset=train_dataset, loss=loss)
trainer.train()
```

For labeled STS, use `CosineSimilarityLoss` and `EmbeddingSimilarityEvaluator`.

For retrieval evaluation, create:

```python
queries = {"q1": "question text"}
corpus = {"d1": "document text"}
relevant_docs = {"q1": {"d1"}}
```

and pass them to `InformationRetrievalEvaluator`.

## CrossEncoder Training

Binary reranker example:

```python
from sentence_transformers import CrossEncoder
from sentence_transformers.cross_encoder.trainer import CrossEncoderTrainer
from sentence_transformers.cross_encoder.training_args import CrossEncoderTrainingArguments
from sentence_transformers.cross_encoder.losses import BinaryCrossEntropyLoss

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", num_labels=1)
loss = BinaryCrossEntropyLoss(model)
args = CrossEncoderTrainingArguments(output_dir="models/reranker", report_to="none")
trainer = CrossEncoderTrainer(model=model, args=args, train_dataset=train_dataset, loss=loss, evaluator=evaluator)
trainer.train()
```

Use `CrossEncoderRerankingEvaluator` for samples containing a query, positives, and negatives. For listwise ranking, use Lambda/List losses and make sure the dataset groups documents by query.

## SparseEncoder Training

Sparse retrieval uses a main ranking loss plus sparsity regularization. A common pattern wraps `SparseMultipleNegativesRankingLoss` in `SpladeLoss`.

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder.losses import SparseMultipleNegativesRankingLoss, SpladeLoss

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
base_loss = SparseMultipleNegativesRankingLoss(model)
loss = SpladeLoss(model, loss=base_loss, document_regularizer_weight=3e-5, query_regularizer_weight=5e-5)
```

Evaluate with `SparseInformationRetrievalEvaluator` and log both ranking metrics and sparsity/active dimensions.

## Hard Negative Mining

Use hard negatives when positives are too easy or retrieval training stalls.

```python
from sentence_transformers.util import mine_hard_negatives

mined = mine_hard_negatives(
    dataset,
    model,
    anchor_column_name="query",
    positive_column_name="positive",
    num_negatives=5,
    output_format="triplet",
    use_faiss=True,
)
```

Filter false negatives using score margins and, when available, a CrossEncoder.

## Smoke-Test Pattern

Before long training:

```python
args.max_steps = 1
args.save_strategy = "no"
trainer.train()
```

Then restore full args and train. The smoke test should prove imports, dataset columns, collator, loss forward pass, evaluator, and output directory behavior.

## Metric And Checkpoint Rules

- Use the evaluator's exact metric key in `metric_for_best_model`.
- If loading the best model at end, make `save_steps` compatible with `eval_steps`.
- Name evaluators deliberately; named evaluators prefix metric keys.
- Keep `greater_is_better=True` for ranking/correlation metrics unless minimizing a loss metric.

## Publishing

Use `model.save_pretrained(...)` for local artifacts. Use `model.push_to_hub(...)` after training, wrapped with error handling if the script should complete without credentials.

For ephemeral remote jobs, trainer-level `push_to_hub=True` and `hub_strategy="every_save"` can preserve checkpoints during training.
