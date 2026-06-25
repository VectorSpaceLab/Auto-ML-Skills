# Evaluation API Reference

FlagEmbedding evaluation modules parse command-line options with `transformers.HfArgumentParser` into benchmark-specific eval args plus model args, then instantiate a runner. Most runners inherit shared behavior from the abstract evaluation runner.

## Entrypoints

Use these module names when constructing commands:

```text
FlagEmbedding.evaluation.beir
FlagEmbedding.evaluation.mteb
FlagEmbedding.evaluation.miracl
FlagEmbedding.evaluation.mldr
FlagEmbedding.evaluation.mkqa
FlagEmbedding.evaluation.msmarco
FlagEmbedding.evaluation.air_bench
FlagEmbedding.evaluation.bright
FlagEmbedding.evaluation.custom
```

## Model Loading Behavior

Shared runners load an embedder with `FlagAutoModel.from_finetuned(...)` and optionally a reranker with `FlagAutoReranker.from_finetuned(...)`.

Important model arguments:

- `--embedder_name_or_path` is required for all families.
- `--embedder_model_class` is needed for custom or non-default model architectures; common values include `encoder-only-base`, `encoder-only-m3`, `decoder-only-base`, `decoder-only-icl`, and `decoder-only-pseudo_moe` where supported.
- `--reranker_name_or_path` enables reranking. Omit it for retrieval-only evaluation.
- `--devices` accepts one or more device strings such as `cuda:0 cuda:1`; omit it or use CPU-safe settings when GPUs are unavailable.
- `--cache_dir` is the model cache for most modules; AIR-Bench uses `--model_cache_dir`.
- `--embedder_batch_size`, `--reranker_batch_size`, `--embedder_query_max_length`, `--embedder_passage_max_length`, and `--reranker_max_length` must fit the selected hardware.
- `--query_instruction_for_retrieval`, `--query_instruction_format_for_retrieval`, `--query_instruction_for_rerank`, and related passage instruction args control instruction-wrapped evaluation.

If the task is about direct encode/score APIs instead of benchmark runners, route to `../inference/`.

## Runner Flow

For shared runners, the flow is:

1. Load embedder and optional reranker.
2. Load benchmark-specific corpus, queries, and qrels through a data loader.
3. Retrieve top-k documents for all queries.
4. Save retrieval search results under `--output_dir`.
5. Optionally rerank the retrieved candidates and save reranked results.
6. Compute metrics from saved search results.
7. Write a final JSON or Markdown summary at `--eval_output_path`.

MTEB is different: it delegates task execution to the official `mteb` package and writes a JSON aggregate from MTEB task result files.

AIR-Bench is different: it runs `AIRBench(...).run(...)` and reports search results; leaderboard-style metric computation may require AIR-Bench-specific follow-up tooling.

## Output Artifacts

For shared retrieval modules, `--output_dir` is a search-result root. Results are nested by embedder string and reranker string. A typical retrieval-only path contains:

```text
<output_dir>/<embedder-name>/NoReranker/<dataset-or-split>.json
<output_dir>/<embedder-name>/NoReranker/EVAL/eval_results.json
```

With a reranker, reranked artifacts appear under:

```text
<output_dir>/<embedder-name>/<reranker-name>/<dataset-or-split>.json
<output_dir>/<embedder-name>/<reranker-name>/EVAL/eval_results.json
```

The final summary is controlled by:

- `--eval_output_method markdown` or `--eval_output_method json`.
- `--eval_output_path`, such as `./beir/eval_results.md`.
- `--eval_metrics`, such as `ndcg_at_10 recall_at_100`.

Search result JSON files include metadata like eval name, model name, reranker name, split, optional dataset name, and the per-query search results. The `EVAL/eval_results.json` files contain metric dictionaries that the runner aggregates into the final summary.

## Metrics and Cutoffs

Common metrics include:

- `ndcg_at_10`: ranking quality at 10.
- `recall_at_10`, `recall_at_100`, `recall_at_1000`: whether relevant documents appear in top-k.
- `qa_recall_at_20`: MKQA-style answer recall metric.

Set `--k_values` to include every cutoff needed by `--eval_metrics`. For example, `--eval_metrics ndcg_at_10 recall_at_100` should include `--k_values 10 100`.

## Benchmark-Specific Args

- BEIR adds `--use_special_instructions` to apply benchmark prompts where available.
- MTEB adds `--languages`, `--tasks`, `--task_types`, `--use_special_instructions`, and `--examples_path`; it only saves final aggregate results as JSON.
- BRIGHT adds `--task_type short|long` and defaults special instructions to enabled.
- AIR-Bench uses `--benchmark_version`, `--task_types`, `--domains`, `--languages`, `--splits`, `--cache_dir`, and `--model_cache_dir`.

## Runtime Planning Tips

- Prefer narrow selectors: one BEIR dataset, one MIRACL/MLDR/MKQA language, one MSMARCO split, or one BRIGHT task/split.
- Avoid full benchmark suites by default; many runners evaluate all available dataset names when `--dataset_names` is omitted.
- Use retrieval-only commands first, then add reranking after retrieval artifacts are confirmed.
- On CPU, reduce batch sizes, max lengths, `--search_top_k`, and skip reranking unless the data is tiny.
- Use `--overwrite False` unless the user wants to replace prior artifacts.
