# Evaluation Arguments

Read this for shared and benchmark-specific FlagEmbedding evaluation arguments.

## Shared Eval Arguments

Most modules extend a shared `AbsEvalArgs`:

| Argument | Default | Meaning |
| --- | --- | --- |
| `--eval_name` | `None` | Name of evaluation task |
| `--dataset_dir` | `None` | Local dataset path or download/cache target |
| `--force_redownload` | `False` | Force remote dataset redownload |
| `--dataset_names` | `None` | Dataset names or languages; multiple values allowed |
| `--splits` | `test` | Splits; multiple values allowed |
| `--corpus_embd_save_dir` | `None` | Save corpus embeddings, or skip if `None` |
| `--output_dir` | `./search_results` | Search result output directory |
| `--search_top_k` | `1000` | Initial retrieval top-k |
| `--rerank_top_k` | `100` | Rerank top-k |
| `--cache_path` | `None` | Dataset cache path |
| `--token` | `HF_TOKEN` env or `None` | Hugging Face token |
| `--overwrite` | `False` | Overwrite existing evaluation outputs |
| `--ignore_identical_ids` | `False` | Ignore identical query/doc ids |
| `--k_values` | `[1, 3, 5, 10, 100, 1000]` | Metric cutoffs |
| `--eval_output_method` | `markdown` | `json` or `markdown` |
| `--eval_output_path` | `./eval_results.md` | Aggregated metric output |
| `--eval_metrics` | `ndcg_at_10 recall_at_10` | Metric names |

## Shared Model Arguments

| Argument | Default | Meaning |
| --- | --- | --- |
| `--embedder_name_or_path` | required | Embedder model or path |
| `--embedder_model_class` | `None` | `encoder-only-base`, `encoder-only-m3`, `decoder-only-base`, `decoder-only-icl`, `decoder-only-pseudo_moe` |
| `--normalize_embeddings` | `True` | Normalize embeddings |
| `--pooling_method` | `None` | Pooling override |
| `--use_fp16` | `True` | Use FP16 inference |
| `--devices` | `None` | Device list |
| `--query_instruction_for_retrieval` | `None` | Query instruction |
| `--query_instruction_format_for_retrieval` | `{}` + `{}` | Query instruction format |
| `--examples_for_task` | `None` | ICL examples |
| `--examples_instruction_format` | `{}` + `{}` | ICL example format |
| `--trust_remote_code` | `False` | Allow remote code |
| `--reranker_name_or_path` | `None` | Optional reranker |
| `--reranker_model_class` | `None` | Reranker class |
| `--reranker_peft_path` | `None` | PEFT adapter path |
| `--use_bf16` | `False` | Use BF16 for supported rerankers |
| `--query_instruction_for_rerank` | `None` | Query instruction for reranker |
| `--passage_instruction_for_rerank` | `None` | Passage instruction for reranker |
| `--cache_dir` | `None` | Model cache |
| `--embedder_batch_size` | `3000` | Embedder batch size |
| `--reranker_batch_size` | `3000` | Reranker batch size |
| `--embedder_query_max_length` | `512` | Query max length |
| `--embedder_passage_max_length` | `512` | Passage max length |
| `--truncate_dim` | `None` | Matryoshka truncation dimension |
| `--reranker_query_max_length` | `None` | Reranker query max length |
| `--reranker_max_length` | `512` | Reranker total max length |
| `--normalize` | `False` | Sigmoid-normalize reranker scores |
| `--prompt` | `None` | LLM reranker prompt |
| `--cutoff_layers` | `None` | Layerwise/lightweight layer cutoffs |
| `--compress_ratio` | `1` | Lightweight compression ratio |
| `--compress_layers` | `None` | Lightweight compression layers |

Evaluation argument parsers replace literal `\n` in instruction formats with newline characters.

## Benchmark-Specific Arguments

MTEB adds:

| Argument | Meaning |
| --- | --- |
| `--languages` | Languages, default example uses `eng` |
| `--tasks` | Task names |
| `--task_types` | Task types |
| `--use_special_instructions` | Use bundled prompts |
| `--examples_path` | Use examples for ICL/task prompts |

BEIR adds:

| Argument | Meaning |
| --- | --- |
| `--use_special_instructions` | Use benchmark prompts |

BRIGHT adds:

| Argument | Default | Meaning |
| --- | --- | --- |
| `--task_type` | `short` | `short` or `long` |
| `--use_special_instructions` | `True` | Use benchmark prompts |

AIR-Bench uses the `air_benchmark` package's own eval args plus a model-args dataclass. Its model cache flag is `--model_cache_dir` rather than `--cache_dir`.
