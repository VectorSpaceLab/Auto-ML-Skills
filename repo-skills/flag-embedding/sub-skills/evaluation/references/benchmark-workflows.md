# Benchmark Workflows

FlagEmbedding evaluation entrypoints are Python modules under `FlagEmbedding.evaluation`. Treat public benchmark examples as command patterns, not safe default executions: they can download datasets/models, use GPUs, and run large retrieval/reranking jobs.

## Family Router

| Request | Module | Primary selectors | Notes |
|---|---|---|---|
| BEIR retrieval | `python -m FlagEmbedding.evaluation.beir` | `--dataset_names`, `--splits` | Datasets include `arguana`, `climate-fever`, `cqadupstack`, `dbpedia-entity`, `fever`, `fiqa`, `hotpotqa`, `msmarco`, `nfcorpus`, `nq`, `quora`, `scidocs`, `scifact`, `trec-covid`, `webis-touche2020`. `msmarco` uses `dev`; most others use `test`. Supports `--use_special_instructions`. |
| MTEB leaderboard/task eval | `python -m FlagEmbedding.evaluation.mteb` | `--languages`, `--tasks`, `--task_types` | Uses the official MTEB package and saves only JSON aggregate output. Supports `--use_special_instructions` and `--examples_path`. Embedders only in normal use; reranking is not the usual MTEB path. |
| MIRACL multilingual retrieval | `python -m FlagEmbedding.evaluation.miracl` | `--dataset_names`, `--splits` | Languages include `ar`, `bn`, `en`, `es`, `fa`, `fi`, `fr`, `hi`, `id`, `ja`, `ko`, `ru`, `sw`, `te`, `th`, `zh`, `de`, `yo`. `en` supports `train` and `dev`; other languages support `dev`. |
| MLDR multilingual long-doc retrieval | `python -m FlagEmbedding.evaluation.mldr` | `--dataset_names`, `--splits` | Languages include `ar`, `de`, `en`, `es`, `fr`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `th`, `zh`. Splits are `train`, `dev`, `test`. Long documents often need larger max lengths and more memory. |
| MKQA multilingual QA retrieval | `python -m FlagEmbedding.evaluation.mkqa` | `--dataset_names`, `--splits` | Languages include `en`, `ar`, `fi`, `ja`, `ko`, `ru`, `es`, `sv`, `he`, `th`, `da`, `de`, `fr`, `it`, `nl`, `pl`, `pt`, `hu`, `vi`, `ms`, `km`, `no`, `tr`, `zh_cn`, `zh_hk`, `zh_tw`. Split is `test`. Uses QA-style metrics such as `qa_recall_at_20`. |
| MSMARCO passage/document | `python -m FlagEmbedding.evaluation.msmarco` | `--dataset_names`, `--splits` | Dataset names are `passage` and `document`; splits are `dev`, `dl19`, `dl20`. Full runs are large and frequently network-bound. |
| AIR-Bench | `python -m FlagEmbedding.evaluation.air_bench` | `--benchmark_version`, `--task_types`, `--domains`, `--languages`, `--splits` | Uses AIR-Bench argument names. Data cache uses `--cache_dir`; model cache uses `--model_cache_dir`. The runner produces search results and points metric submission to AIR-Bench tooling. |
| BRIGHT | `python -m FlagEmbedding.evaluation.bright` | `--task_type`, `--dataset_names`, `--splits` | `--task_type` is `short` or `long`. Short datasets include StackExchange, coding, and theorem tasks; long datasets include StackExchange/coding subsets. Supports special instructions by default. Long tasks can require large context lengths. |
| Custom retrieval data | `python -m FlagEmbedding.evaluation.custom` | `--dataset_dir`, `--splits` | Use for local JSONL corpus/query/qrels data. The custom loader has no dataset names and defaults to `test`. |

## Shared Evaluation Arguments

Most non-AIR-Bench families share these evaluation controls:

- `--eval_name`: logical run name, usually the benchmark id such as `beir`, `mldr`, or `custom`.
- `--dataset_dir`: local dataset root or a destination where remote data may be saved. If omitted for supported public benchmarks, loaders can fetch remote data through dataset APIs.
- `--dataset_names`: benchmark-specific dataset names or languages. If omitted, many runners evaluate all available names, which is rarely safe by default.
- `--splits`: one or more split names such as `test`, `dev`, `dl19`, or `examples`.
- `--corpus_embd_save_dir`: optional corpus embedding cache; useful for repeated runs but can be large.
- `--output_dir`: search result root. Results are nested by embedder and reranker names.
- `--search_top_k` and `--rerank_top_k`: retrieval and reranking fanout; lower them for dry runs or CPU.
- `--cache_path`: dataset cache for non-AIR-Bench modules.
- `--overwrite`: whether to replace existing search/eval outputs.
- `--ignore_identical_ids`: useful for retrieval tasks where query ids and document ids overlap.
- `--k_values`, `--eval_metrics`, `--eval_output_method`, `--eval_output_path`: metric cutoffs and final summary output.

Shared model controls include `--embedder_name_or_path`, optional `--embedder_model_class`, `--normalize_embeddings`, `--pooling_method`, `--use_fp16`, `--use_bf16`, `--devices`, retrieval/reranking instructions, optional `--reranker_name_or_path`, optional `--reranker_model_class`, model `--cache_dir`, batch sizes, max lengths, and reranker-specific compression/layer options.

AIR-Bench differs: it uses AIR-Bench eval args, `--cache_dir` for benchmark data, and `--model_cache_dir` for model artifacts.

## Custom Dataset Layout

A local custom dataset directory must contain these JSONL files for each split:

- `corpus.jsonl`: each row has `id` and `text`; `title` is optional for retrieval datasets.
- `<split>_queries.jsonl`: each row has `id` and `text`.
- `<split>_qrels.jsonl`: each row has `qid`, `docid`, and `relevance`.

Example directory for `--splits test dev`:

```text
my_eval_data/
  corpus.jsonl
  test_queries.jsonl
  test_qrels.jsonl
  dev_queries.jsonl
  dev_qrels.jsonl
```

Before generating a command, verify that every qrels `qid` exists in the corresponding queries file and every qrels `docid` exists in `corpus.jsonl`. Missing ids cause empty metrics, loader errors, or misleading zero scores.

## Safe Planning Pattern

When a user asks for a benchmark without enough execution detail, return a safe plan instead of running:

1. State the module and selectors you would use.
2. Ask for or choose a narrow subset such as one BEIR dataset, one MIRACL/MLDR language, or one MTEB task.
3. Require explicit cache/output paths.
4. Include a generated command.
5. Mark execution as skipped until the user approves downloads/runtime.

Use `scripts/build_eval_command.py` to avoid hand-copying long module invocations.
