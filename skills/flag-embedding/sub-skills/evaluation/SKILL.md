---
name: evaluation
description: "Helps agents run FlagEmbedding benchmark and custom retrieval evaluation modules with embedders, rerankers, and retrieval metrics."
disable-model-invocation: true
---

# FlagEmbedding Evaluation

Use this sub-skill when the user wants to evaluate a FlagEmbedding embedder or reranker on MTEB, BEIR, MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, or a custom retrieval dataset.

## Install Dependencies

Base package:

```bash
python -m pip install -U FlagEmbedding
```

Common evaluation extras:

```bash
python -m pip install pytrec_eval
python -m pip install beir
python -m pip install mteb==1.15.0
```

If `pytrec_eval` fails, try `pytrec-eval-terrier`. Install a FAISS build compatible with the target Python/CUDA environment when retrieval indexing is required.

## Evaluation Modules

Run evaluations with `python -m`:

| Benchmark | Module |
| --- | --- |
| MTEB | `FlagEmbedding.evaluation.mteb` |
| BEIR | `FlagEmbedding.evaluation.beir` |
| MSMARCO | `FlagEmbedding.evaluation.msmarco` |
| MIRACL | `FlagEmbedding.evaluation.miracl` |
| MLDR | `FlagEmbedding.evaluation.mldr` |
| MKQA | `FlagEmbedding.evaluation.mkqa` |
| AIR-Bench | `FlagEmbedding.evaluation.air_bench` |
| BRIGHT | `FlagEmbedding.evaluation.bright` |
| Custom dataset | `FlagEmbedding.evaluation.custom` |

Read [references/evaluation-workflows.md](references/evaluation-workflows.md) for benchmark-specific commands and dataset name/split notes.

## Shared Argument Pattern

Most evaluation modules use:

```bash
python -m FlagEmbedding.evaluation.beir \
  --eval_name beir \
  --dataset_dir ./beir/data \
  --dataset_names fiqa arguana \
  --splits test \
  --corpus_embd_save_dir ./beir/corpus_embd \
  --output_dir ./beir/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./beir/eval_results.md \
  --eval_metrics ndcg_at_10 recall_at_100 \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 \
  --cache_dir ./cache/model \
  --reranker_max_length 1024
```

## Custom Dataset

Custom evaluation data must contain:

```text
corpus.jsonl
<split>_queries.jsonl
<split>_qrels.jsonl
```

or multiple child directories each containing those files. Read [references/data-formats.md](references/data-formats.md) and run:

```bash
python scripts/check_eval_dataset.py --dataset-dir ./my_eval_data --splits test
```

## References

Read [references/evaluation-workflows.md](references/evaluation-workflows.md) for commands for every supported evaluation module.

Read [references/arguments.md](references/arguments.md) for shared `EvalArgs`, `ModelArgs`, and benchmark-specific argument notes.

Read [references/data-formats.md](references/data-formats.md) for custom evaluation file schemas.

Read [references/troubleshooting.md](references/troubleshooting.md) for dependency, dataset, metric, and memory failures.

## Scripts

Run [scripts/check_eval_dataset.py](scripts/check_eval_dataset.py) to verify custom dataset layout before running a benchmark.

Read or adapt [scripts/build_eval_command.py](scripts/build_eval_command.py) to print a conservative evaluation command for common benchmarks.
