# Evaluation CLI Reference

Read this for module names, common arguments, benchmark-specific arguments, and command recipes.

## Modules

All commands use `python -m`:

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
| Custom | `FlagEmbedding.evaluation.custom` |

## Common Evaluation Arguments

- `--eval_name`: task name such as `beir`, `msmarco`, or `custom`.
- `--dataset_dir`: local dataset directory or download/cache target. For custom datasets it must exist.
- `--force_redownload`: redownload remote datasets.
- `--dataset_names`: dataset names or languages; multiple values accepted.
- `--splits`: split names; default is `test`.
- `--corpus_embd_save_dir`: save corpus embeddings for reuse; omit to avoid saving.
- `--output_dir`: search-result output directory.
- `--search_top_k`: initial retrieval cutoff, default `1000`.
- `--rerank_top_k`: reranking cutoff, default `100`.
- `--cache_path`: dataset cache path.
- `--token`: Hugging Face token; defaults to `HF_TOKEN`.
- `--overwrite`: overwrite previous outputs.
- `--ignore_identical_ids`: ignore same query/doc ids when evaluating.
- `--k_values`: metric cutoffs.
- `--eval_output_method`: `json` or `markdown`.
- `--eval_output_path`: metric output file.
- `--eval_metrics`: metrics such as `ndcg_at_10` or `recall_at_100`.

## Common Model Arguments

- `--embedder_name_or_path`: required embedder id/path.
- `--embedder_model_class`: one of `encoder-only-base`, `encoder-only-m3`, `decoder-only-base`, `decoder-only-icl`, `decoder-only-pseudo_moe`.
- `--normalize_embeddings`: default `True`.
- `--pooling_method`: custom pooling method when needed.
- `--use_fp16`: default `True`.
- `--devices`: one or more devices.
- `--query_instruction_for_retrieval`, `--query_instruction_format_for_retrieval`.
- `--examples_for_task`, `--examples_instruction_format`.
- `--trust_remote_code`.
- `--reranker_name_or_path`: optional reranker id/path.
- `--reranker_model_class`: one of `encoder-only-base`, `decoder-only-base`, `decoder-only-layerwise`, `decoder-only-lightweight`.
- `--reranker_peft_path`.
- `--use_bf16`.
- `--query_instruction_for_rerank`, `--passage_instruction_for_rerank` and their format flags.
- `--cache_dir`: model cache.
- `--embedder_batch_size`, `--reranker_batch_size`.
- `--embedder_query_max_length`, `--embedder_passage_max_length`.
- `--truncate_dim`: Matryoshka truncation dimension.
- `--reranker_query_max_length`, `--reranker_max_length`.
- `--normalize`: normalize reranker scores.
- `--prompt`.
- `--cutoff_layers`, `--compress_ratio`, `--compress_layers`.

## MTEB

Extra flags:

- `--languages`
- `--tasks`
- `--task_types`
- `--use_special_instructions`
- `--examples_path`

Example:

```bash
python -m FlagEmbedding.evaluation.mteb \
  --eval_name mteb \
  --output_dir ./data/mteb/search_results \
  --languages eng \
  --tasks NFCorpus BiorxivClusteringS2S SciDocsRR \
  --eval_output_path ./mteb/mteb_eval_results.json \
  --embedder_name_or_path BAAI/bge-m3 \
  --devices cuda:0 \
  --cache_dir ./cache/model
```

## BEIR

Extra flag:

- `--use_special_instructions`

Example:

```bash
python -m FlagEmbedding.evaluation.beir \
  --eval_name beir \
  --dataset_dir ./beir/data \
  --dataset_names fiqa arguana cqadupstack \
  --splits test dev \
  --corpus_embd_save_dir ./beir/corpus_embd \
  --output_dir ./beir/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./beir/beir_eval_results.md \
  --eval_metrics ndcg_at_10 recall_at_100 \
  --ignore_identical_ids True \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --cache_dir ./cache/model \
  --reranker_query_max_length 512 \
  --reranker_max_length 1024
```

## MSMARCO

Common dataset names include `passage` and `document`; common splits include `dev`, `dl19`, and `dl20`.

```bash
python -m FlagEmbedding.evaluation.msmarco \
  --eval_name msmarco \
  --dataset_dir ./msmarco/data \
  --dataset_names passage \
  --splits dev dl19 dl20 \
  --corpus_embd_save_dir ./msmarco/corpus_embd \
  --output_dir ./msmarco/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --eval_output_path ./msmarco/msmarco_eval_results.md \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3
```

## MIRACL, MLDR, And MKQA

Use `--dataset_names` for languages.

MIRACL example language names include `ar`, `bn`, `en`, `es`, `fa`, `fi`, `fr`, `hi`, `id`, `ja`, `ko`, `ru`, `sw`, `te`, `th`, `zh`, `de`, and `yo`.

MLDR example language names include `ar`, `de`, `en`, `es`, `fr`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `th`, and `zh`.

MKQA example language names include `en`, `ar`, `fi`, `ja`, `ko`, `ru`, `es`, `sv`, `he`, `th`, `da`, `de`, `fr`, `it`, `nl`, `pl`, `pt`, `hu`, `vi`, `ms`, `km`, `no`, `tr`, `zh_cn`, `zh_hk`, and `zh_tw`.

## AIR-Bench

AIR-Bench uses its official argument class. Important flags include:

- `--benchmark_version`
- `--task_types`
- `--domains`
- `--languages`

Example:

```bash
python -m FlagEmbedding.evaluation.air_bench \
  --benchmark_version AIR-Bench_24.05 \
  --task_types qa long-doc \
  --domains arxiv \
  --languages en \
  --splits dev test \
  --output_dir ./air_bench/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --embedder_name_or_path BAAI/bge-m3
```

After running, AIR-Bench prints guidance that search results were generated and metrics should follow the official AIR-Bench submission/evaluation docs.

## BRIGHT

Extra flags:

- `--task_type`: `short` or `long`.
- `--use_special_instructions`: default `True` in the argument class.

## Custom

Use the custom module when the user has local files in the expected layout:

```bash
python -m FlagEmbedding.evaluation.custom \
  --eval_name custom \
  --dataset_dir ./my_eval \
  --splits test \
  --output_dir ./my_eval/search_results \
  --eval_output_path ./my_eval/eval_results.md \
  --embedder_name_or_path BAAI/bge-m3
```

Validate the dataset before running:

```bash
python scripts/validate_custom_eval_dataset.py ./my_eval --splits test
```
