---
name: evaluation
description: "Use for FlagEmbedding retrieval evaluation on MTEB, BEIR, MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, or custom datasets, including CLI flags, dataset layout, metrics, and evaluation troubleshooting."
---

# FlagEmbedding Evaluation

Use this sub-skill when the user wants to evaluate a FlagEmbedding embedder, optionally rerank search results, run retrieval benchmarks, prepare a custom evaluation dataset, choose metrics, or debug benchmark dependencies.

## Install

Base package:

```bash
python -m pip install -U FlagEmbedding
```

Benchmark-specific extras are installed separately as needed:

```bash
python -m pip install mteb==1.15.0
python -m pip install beir
python -m pip install pytrec_eval
python -m pip install pytrec-eval-terrier
python -m pip install air-benchmark
```

FAISS package selection depends on Python, CUDA, and platform. Choose CPU or GPU wheels deliberately instead of copying a wheel URL blindly.

## Read These First

- `references/cli-reference.md` for supported `python -m FlagEmbedding.evaluation.*` modules, common flags, model args, benchmark-specific flags, and command recipes.
- `references/data-formats.md` for custom dataset layout and JSONL schemas.
- `references/troubleshooting.md` for missing dependencies, dataset layout errors, stale outputs, cache behavior, and metric/output issues.

Run:

- `scripts/validate_custom_eval_dataset.py` before a custom evaluation.

## Evaluation Modules

Use these module names:

- `FlagEmbedding.evaluation.mteb`
- `FlagEmbedding.evaluation.beir`
- `FlagEmbedding.evaluation.msmarco`
- `FlagEmbedding.evaluation.miracl`
- `FlagEmbedding.evaluation.mldr`
- `FlagEmbedding.evaluation.mkqa`
- `FlagEmbedding.evaluation.air_bench`
- `FlagEmbedding.evaluation.bright`
- `FlagEmbedding.evaluation.custom`

Every module parses dataclass arguments with Hugging Face `HfArgumentParser`.

## Common Command Shape

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
  --reranker_query_max_length 512 \
  --reranker_max_length 1024
```

## Custom Dataset Layout

A custom dataset directory should contain these files for each split:

```text
dataset_dir/
  corpus.jsonl
  test_queries.jsonl
  test_qrels.jsonl
```

or multiple dataset subdirectories each with the same files.

Validate:

```bash
python scripts/validate_custom_eval_dataset.py ./my_eval_data --splits test
```

## Benchmark Choice

- MTEB: embedding benchmark tasks; official MTEB output is JSON.
- BEIR: retrieval datasets such as arguana, fiqa, nfcorpus, scifact, trec-covid, and others.
- MSMARCO: passage/document retrieval with dev/dl19/dl20 splits.
- MIRACL: multilingual retrieval by language.
- MLDR: multilingual long-document retrieval.
- MKQA: cross-lingual QA retrieval.
- AIR-Bench: official AIR-Bench evaluation integration; generated search results may require official metric submission flow.
- BRIGHT: short/long task types with special instructions enabled by default in its argument class.
- Custom: local corpus/query/qrels layout.

## Safety

Evaluation can download datasets, cache embeddings, and write result directories. Do not run it unless the user asks for those side effects and the target output/cache paths are clear.
