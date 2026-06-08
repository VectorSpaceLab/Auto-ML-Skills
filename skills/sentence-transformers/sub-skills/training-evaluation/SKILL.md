---
name: training-evaluation
description: "Train, fine-tune, evaluate, and debug SentenceTransformer, CrossEncoder, and SparseEncoder models with trainers, losses, evaluators, dataset formats, hard negatives, and Hub publishing."
---

# Training And Evaluation

Use this sub-skill for fine-tuning and evaluating embedding models, rerankers, and sparse encoders with the `sentence-transformers` trainer APIs.

If the repo-local `train-sentence-transformers` skill is available, use it for production-grade training scripts and deeper loss/evaluator templates. This sub-skill remains self-contained for model-type selection, public APIs, and ordinary workflows.

## Required Reading

- `references/api-reference.md`: verified trainer, training args, loss, and evaluator signatures.
- `references/workflows.md`: data shapes, loss/evaluator selection, hard-negative mining, and training skeletons.
- `scripts/inspect_training_api.py`: safe live API inspection helper for installed environments.

Read root `../../references/troubleshooting.md` for install/backend issues.

## Install

```bash
pip install -U "sentence-transformers[train]"
pip install trackio       # optional tracker
pip install codecarbon    # optional model-card emissions tracking
```

For Hub publishing, authenticate with a write-capable token before training or pushing.

## Choose The Model Family

| Goal | Class | Trainer | Common losses/evaluators |
| --- | --- | --- | --- |
| dense embedding retrieval, STS, clustering features | `SentenceTransformer` | `SentenceTransformerTrainer` | `MultipleNegativesRankingLoss`, `CosineSimilarityLoss`, `TripletLoss`, `InformationRetrievalEvaluator`, `EmbeddingSimilarityEvaluator` |
| reranker or pair classifier | `CrossEncoder` | `CrossEncoderTrainer` | `BinaryCrossEntropyLoss`, `CrossEntropyLoss`, `LambdaLoss`, `CrossEncoderRerankingEvaluator` |
| SPLADE / learned sparse retrieval | `SparseEncoder` | `SparseEncoderTrainer` | `SpladeLoss`, `SparseMultipleNegativesRankingLoss`, `CSRLoss`, `SparseInformationRetrievalEvaluator` |

Ask for the task, labels, and dataset columns if they are unclear. Loss choice depends primarily on the data shape.

## Dataset Shape Rules

- Pair contrastive retrieval: `(anchor, positive)` or `(query, positive_document)` -> MultipleNegativesRanking-style losses.
- Triplets: `(anchor, positive, negative)` -> triplet losses or MNRL variants that accept explicit negatives.
- Labeled similarity: `(sentence1, sentence2, score)` -> cosine/MSE-style losses and embedding similarity evaluation.
- CrossEncoder binary relevance: `(query, document, label)` -> binary cross entropy.
- CrossEncoder listwise ranking: query with multiple docs and relevance labels -> Lambda/List losses.
- Sparse SPLADE retrieval: usually query/document pairs plus a sparse regularization wrapper.

When using in-batch negatives, avoid duplicate positives in the same batch; use the appropriate no-duplicates batch sampler when needed.

## Training Skeleton

```python
from datasets import Dataset
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.losses import MultipleNegativesRankingLoss
from sentence_transformers import SentenceTransformerTrainer, SentenceTransformerTrainingArguments

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
train_dataset = Dataset.from_dict({
    "anchor": ["What is Python?"],
    "positive": ["Python is a programming language."],
})
loss = MultipleNegativesRankingLoss(model)
args = SentenceTransformerTrainingArguments(
    output_dir="models/my-embedding-model",
    num_train_epochs=1,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
    warmup_steps=0.1,
    eval_strategy="no",
    save_strategy="epoch",
    report_to="none",
)
trainer = SentenceTransformerTrainer(model=model, args=args, train_dataset=train_dataset, loss=loss)
trainer.train()
model.save_pretrained("models/my-embedding-model/final")
```

For real training, add an evaluator, baseline evaluation, smoke run, logging, and Hub push/error handling.

## Production Habits

- Run a tiny smoke test (`max_steps=1`) before a long run.
- Evaluate before and after training using the metric that matches the task.
- Save the exact base model id, dataset revision, prompts, loss, evaluator, batch sampler, and metric names.
- Use `metric_for_best_model` that exactly matches evaluator output keys.
- Prefer loading the base model in full precision and using trainer `bf16`/`fp16` autocast rather than forcing low-precision weights blindly.
- For CrossEncoder rerankers, watch for mid-training regression and consider early stopping.
- For SparseEncoder, log active dimensions and sparsity alongside ranking metrics.
