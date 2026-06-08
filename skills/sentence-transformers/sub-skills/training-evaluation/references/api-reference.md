# Training And Evaluation API Reference

Read this for verified trainer, argument, loss, and evaluator signatures.

## Trainers

```python
SentenceTransformerTrainer(
    model=None,
    args=None,
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

`CrossEncoderTrainer` and `SparseEncoderTrainer` have the same shape with their corresponding model, arguments, and data collator classes.

## Training Arguments

`SentenceTransformerTrainingArguments`, `CrossEncoderTrainingArguments`, and `SparseEncoderTrainingArguments` extend Transformers training arguments with sentence-transformers-specific fields.

Important common fields:

```python
output_dir
per_device_train_batch_size=8
num_train_epochs=3.0
max_steps=-1
learning_rate=5e-5
warmup_steps=0
bf16=False
fp16=False
gradient_checkpointing=False
logging_steps=500
report_to="none"
eval_strategy="no"
eval_steps=None
save_strategy="steps"
save_steps=500
load_best_model_at_end=False
metric_for_best_model=None
push_to_hub=False
hub_model_id=None
seed=42
batch_sampler=BatchSamplers.BATCH_SAMPLER
multi_dataset_batch_sampler=MultiDatasetBatchSamplers.PROPORTIONAL
prompts=None
router_mapping={}
learning_rate_mapping={}
```

`warmup_steps` can be a float ratio. If `load_best_model_at_end=True`, save/eval strategies and steps must be compatible.

## Dense Losses And Evaluators

```python
MultipleNegativesRankingLoss(
    model,
    scale=20.0,
    similarity_fct=cos_sim,
    gather_across_devices=False,
    directions=("query_to_doc",),
    partition_mode="joint",
    hardness_mode=None,
    hardness_strength=0.0,
)
```

```python
CosineSimilarityLoss(model, loss_fct=MSELoss(), cos_score_transformation=Identity())
TripletLoss(model, distance_metric=..., triplet_margin=5)
```

```python
EmbeddingSimilarityEvaluator(
    sentences1,
    sentences2,
    scores,
    batch_size=16,
    main_similarity=None,
    similarity_fn_names=None,
    name="",
    show_progress_bar=False,
    write_csv=True,
    precision=None,
    truncate_dim=None,
)
```

```python
InformationRetrievalEvaluator(
    queries,
    corpus,
    relevant_docs,
    corpus_chunk_size=50000,
    mrr_at_k=[10],
    ndcg_at_k=[10],
    accuracy_at_k=[1, 3, 5, 10],
    precision_recall_at_k=[1, 3, 5, 10],
    map_at_k=[100],
    batch_size=32,
    name="",
    score_functions=None,
    main_score_function=None,
    query_prompt_name=None,
    corpus_prompt_name=None,
    write_predictions=False,
)
```

## CrossEncoder Losses And Evaluators

```python
BinaryCrossEntropyLoss(model, activation_fn=Identity(), pos_weight=None, **kwargs)
CrossEntropyLoss(model, activation_fn=Identity(), **kwargs)
LambdaLoss(model, weighting_scheme=..., k=None, sigma=1.0, eps=1e-10, reduction_log="binary", activation_fn=Identity(), mini_batch_size=None)
```

```python
CrossEncoderRerankingEvaluator(
    samples,
    at_k=10,
    always_rerank_positives=True,
    name="",
    prompt_name=None,
    batch_size=64,
    show_progress_bar=False,
    write_csv=True,
    mrr_at_k=None,
)
```

## Sparse Losses And Evaluators

```python
SpladeLoss(
    model,
    loss,
    document_regularizer_weight,
    query_regularizer_weight=None,
    document_regularizer=None,
    query_regularizer=None,
    document_regularizer_threshold=None,
    query_regularizer_threshold=None,
    use_document_regularizer_only=False,
)
```

```python
SparseMultipleNegativesRankingLoss(
    model,
    scale=1.0,
    similarity_fct=dot_score,
    gather_across_devices=False,
    directions=("query_to_doc",),
    partition_mode="joint",
    hardness_mode=None,
    hardness_strength=0.0,
)
```

```python
CSRLoss(model, loss=None, beta=0.1, gamma=1.0)
```

```python
SparseInformationRetrievalEvaluator(
    queries,
    corpus,
    relevant_docs,
    corpus_chunk_size=50000,
    mrr_at_k=[10],
    ndcg_at_k=[10],
    accuracy_at_k=[1, 3, 5, 10],
    precision_recall_at_k=[1, 3, 5, 10],
    map_at_k=[100],
    batch_size=32,
    name="",
    max_active_dims=None,
    score_functions=None,
    main_score_function=None,
    query_prompt_name=None,
    corpus_prompt_name=None,
    write_predictions=False,
)
```

## Hard Negative Mining

```python
mine_hard_negatives(
    dataset,
    model,
    anchor_column_name=None,
    positive_column_name=None,
    corpus=None,
    cross_encoder=None,
    range_min=0,
    range_max=None,
    max_score=None,
    min_score=None,
    absolute_margin=None,
    relative_margin=None,
    num_negatives=3,
    sampling_strategy="top",
    query_prompt_name=None,
    corpus_prompt_name=None,
    include_positives=False,
    output_format="triplet",
    output_scores=False,
    batch_size=32,
    faiss_batch_size=16384,
    use_faiss=False,
    use_multi_process=False,
    verbose=True,
    cache_folder=None,
)
```
