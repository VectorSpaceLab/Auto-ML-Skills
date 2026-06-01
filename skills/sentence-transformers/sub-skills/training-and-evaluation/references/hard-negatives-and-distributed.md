# Hard Negatives And Distributed Training

## Hard Negative Mining

Use `mine_hard_negatives` to convert positive-pair datasets into training formats with challenging negatives.

Verified signature:

```python
mine_hard_negatives(
    dataset,
    model,
    anchor_column_name: str | None = None,
    positive_column_name: str | None = None,
    corpus: list[str] | None = None,
    cross_encoder: CrossEncoder | None = None,
    range_min: int = 0,
    range_max: int | None = None,
    max_score: float | None = None,
    min_score: float | None = None,
    absolute_margin: float | None = None,
    relative_margin: float | None = None,
    num_negatives: int = 3,
    sampling_strategy: Literal["random", "top"] = "top",
    query_prompt_name: str | None = None,
    query_prompt: str | None = None,
    corpus_prompt_name: str | None = None,
    corpus_prompt: str | None = None,
    include_positives: bool = False,
    output_format: Literal["triplet", "n-tuple", "labeled-pair", "labeled-list"] = "triplet",
    output_scores: bool = False,
    batch_size: int = 32,
    faiss_batch_size: int = 16384,
    use_faiss: bool = False,
    use_multi_process: list[str] | bool = False,
    verbose: bool = True,
    cache_folder: str | None = None,
) -> Dataset
```

Common output formats:

- `triplet`: `anchor`, `positive`, `negative`.
- `n-tuple`: `anchor`, `positive`, `negative_1`, ..., `negative_n`.
- `labeled-pair`: query/document pairs with 0/1 labels.
- `labeled-list`: query with a list of documents and labels, useful for listwise reranker losses.

## Mining Guidance

Hard negatives should be close enough to be challenging but not false negatives. Use score thresholds or margins when the mined negatives include true positives.

If using a reranker as `cross_encoder`, it can filter or score candidate negatives more accurately but adds compute.

Use `use_faiss=True` for large corpora when FAISS is installed.

## Distributed Training

For multi-GPU training, put the training script in a `main()` function and call it under:

```python
if __name__ == "__main__":
    main()
```

Then use `torchrun` or `accelerate launch` depending on the environment:

```bash
torchrun --nproc_per_node 4 train.py
accelerate launch train.py
```

Avoid top-level dataset downloads, model creation, or trainer execution outside `main()` because each worker imports/runs the script.

## Large Batch Patterns

For in-batch-negative losses, larger effective batch size often improves quality. Options:

- increase per-device batch size;
- use gradient accumulation;
- use cached losses such as `CachedMultipleNegativesRankingLoss` or `CachedSpladeLoss`;
- use distributed training.

Cached losses can improve effective batch size without proportional memory growth, but they add complexity and may change throughput.

## Router Models

For query/document routers or multimodal routers, set `router_mapping` so columns feed the right route:

```python
args = SentenceTransformerTrainingArguments(
    output_dir="...",
    router_mapping={"question": "query", "answer": "document"},
)
```

Missing router mappings can silently train the wrong path or fail at preprocessing time.
