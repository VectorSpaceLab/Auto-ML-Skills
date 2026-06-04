# Evaluation

Use evaluators during training and as standalone quality checks. Select the evaluator from the task metric, not just the model family.

## Dense Evaluators

Dense evaluator classes include:

- `EmbeddingSimilarityEvaluator`: STS-style correlation between pair scores and embedding similarities.
- `InformationRetrievalEvaluator`: query/corpus/relevance retrieval metrics such as NDCG, MRR, MAP, recall.
- `RerankingEvaluator`: evaluate reranking candidate lists using dense models.
- `BinaryClassificationEvaluator`: binary pair classification using embedding similarities.
- `TripletEvaluator`: anchor-positive-negative accuracy.
- `ParaphraseMiningEvaluator`: paraphrase mining quality.
- `TranslationEvaluator`: bitext retrieval / translation matching.
- `MSEEvaluator` and `MSEEvaluatorFromDataFrame`: embedding distillation.
- `LabelAccuracyEvaluator`: classification label accuracy.
- `NanoBEIREvaluator`: small BEIR-style retrieval benchmark.
- `SequentialEvaluator`: run several evaluators together.

## Cross Encoder Evaluators

Cross Encoder evaluator classes include:

- `CrossEncoderRerankingEvaluator` / `CERerankingEvaluator`.
- `CrossEncoderCorrelationEvaluator` / `CECorrelationEvaluator`.
- `CrossEncoderClassificationEvaluator`.
- `CEBinaryClassificationEvaluator`.
- `CEBinaryAccuracyEvaluator`.
- `CEF1Evaluator`.
- `CESoftmaxAccuracyEvaluator`.
- `CrossEncoderNanoBEIREvaluator`.

Use reranking evaluators for search ranking, not correlation evaluators.

## Sparse Evaluators

Sparse evaluator classes include:

- `SparseInformationRetrievalEvaluator`.
- `SparseRerankingEvaluator`.
- `SparseEmbeddingSimilarityEvaluator`.
- `SparseBinaryClassificationEvaluator`.
- `SparseTripletEvaluator`.
- `SparseTranslationEvaluator`.
- `SparseMSEEvaluator`.
- `SparseNanoBEIREvaluator`.
- `ReciprocalRankFusionEvaluator` for hybrid sparse/dense fusion evaluation.

## Choosing Metrics

Retrieval:

- NDCG@k for graded relevance and ranking quality.
- MRR@k for first relevant result.
- Recall@k for candidate-generation coverage.
- MAP for average precision across relevant documents.

Reranking:

- NDCG/MRR/MAP on candidate lists.
- Compare before and after reranker to prove improvement.

STS:

- Spearman/Pearson correlation.

Classification:

- Accuracy, F1, binary classification metrics.

Sparse:

- Retrieval metrics plus sparsity/active dimension summaries.

## Evaluator In Trainer

Pass an evaluator to the trainer:

```python
trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=evaluator,
)
```

Set `eval_strategy` and `eval_steps` or run `evaluator(model)` manually after training.

## Common Mistake

Do not evaluate only on training loss. For retrieval, a held-out query/corpus/relevance set is the useful signal.
