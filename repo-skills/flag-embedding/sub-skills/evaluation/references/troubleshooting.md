# Evaluation Troubleshooting

Use this guide to diagnose FlagEmbedding evaluation setup problems without accidentally starting expensive downloads or benchmark runs.

## Datasets or Corpora Not Downloaded

Symptoms:

- Loader errors mention missing `corpus.jsonl`, `<split>_queries.jsonl`, or `<split>_qrels.jsonl`.
- Hugging Face dataset download errors appear.
- Public benchmark command starts fetching many files.

Safe response:

1. Stop and report that execution would require dataset download or a prepared local dataset.
2. Ask the user to provide a local `--dataset_dir` or approve downloads and cache location.
3. Generate the command plan with explicit `--dataset_dir` and `--cache_path` or AIR-Bench `--cache_dir`.
4. Do not use private tokens unless the user explicitly confirms credentials are configured.

## Credentials or Private Access Missing

Symptoms:

- HTTP 401/403 errors.
- Dataset or model repository not found despite a valid name.
- Errors mention `HF_TOKEN`, gated models, or private datasets.

Safe response:

- Tell the user to authenticate through their own environment and rerun.
- Avoid printing tokens or embedding credentials in commands.
- For model access issues, generate a retrieval-only command using a local model path if the user provides one.

## Benchmark Is Too Expensive

Symptoms:

- Request asks for all BEIR, all MTEB, all languages, or reranked MSMARCO/AIR-Bench/BRIGHT.
- CPU-only environment but command uses large models, large corpora, high top-k, or long max lengths.
- Multiple `cuda:*` devices are requested but unavailable.

Safe response:

- Skip execution and present a staged plan: small retrieval-only subset first, then larger subsets, then reranking.
- Lower `--search_top_k`, `--rerank_top_k`, batch sizes, and max lengths for smoke tests.
- Omit `--reranker_name_or_path` until retrieval outputs and runtime are confirmed.
- For MLDR/BRIGHT long tasks, call out long document lengths and memory pressure.

## Wrong Dataset, Language, Task, or Split

Symptoms:

- Errors say dataset name or split not found.
- The runner silently skips because no checked split is valid.
- MTEB returns no tasks.

Safe response:

- Validate selectors against the family:
  - BEIR: public dataset names such as `fiqa`, `arguana`, `nq`; `msmarco` uses `dev`, most others use `test`.
  - MIRACL: language codes include `ar`, `bn`, `en`, `es`, `fa`, `fi`, `fr`, `hi`, `id`, `ja`, `ko`, `ru`, `sw`, `te`, `th`, `zh`, `de`, `yo`; `en` supports `train` and `dev`, others `dev`.
  - MLDR: language codes include `ar`, `de`, `en`, `es`, `fr`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `th`, `zh`; splits are `train`, `dev`, `test`.
  - MKQA: split is `test`; language variants include `zh_cn`, `zh_hk`, and `zh_tw`.
  - MSMARCO: dataset names are `passage` or `document`; splits are `dev`, `dl19`, `dl20`.
  - BRIGHT: `--task_type` must be `short` or `long`; common split values include `examples`, `gpt4_reason`, `grit_reason`, and model-reasoning split names.
- For MTEB, narrow by `--tasks` or `--task_types` and verify the requested language code follows MTEB naming.

## Custom Dataset ID Mismatches

Symptoms:

- Metrics are zero despite apparently relevant data.
- Key errors happen during qrels or query lookup.
- Search result files contain fewer query ids than expected.

Checklist:

- `corpus.jsonl` rows contain unique string-compatible `id` values and `text`.
- `<split>_queries.jsonl` rows contain unique `id` values and `text`.
- `<split>_qrels.jsonl` rows contain `qid`, `docid`, and numeric `relevance`.
- Every qrels `qid` appears in the matching queries file.
- Every qrels `docid` appears in `corpus.jsonl`.
- Split names in files match `--splits` exactly.
- If query ids overlap document ids, decide whether `--ignore_identical_ids True` is appropriate.

## Model Cache, Token, or Network Failures

Symptoms:

- Model loading errors from Transformers or Hugging Face Hub.
- Network timeouts, DNS errors, proxy errors, or incomplete cache files.
- Trust-remote-code errors for models requiring custom code.

Safe response:

- Ask whether to use a local model path or retry downloads.
- Keep `--cache_dir` or `--model_cache_dir` explicit and portable.
- Only add `--trust_remote_code True` if the user accepts remote model code execution risk.
- Do not delete caches unless the user asks; suggest a separate clean cache path for repro.

## GPU/CPU, Batch, and Max-Length Problems

Symptoms:

- CUDA out-of-memory, process killed, or very slow CPU execution.
- Tokenizer/model warnings about truncation.
- Long-document benchmarks fail with sequence length limits.

Safe response:

- Reduce `--embedder_batch_size` and `--reranker_batch_size`.
- Reduce `--embedder_passage_max_length`, `--embedder_query_max_length`, and `--reranker_max_length`, unless benchmark validity requires long context.
- Remove `--devices cuda:*` when GPUs are unavailable.
- Prefer retrieval-only smoke tests before reranking.
- For BRIGHT/MLDR long-document workflows, explicitly balance max length against available memory.

## Output Already Exists or Looks Stale

Symptoms:

- Run reuses old search results because `--overwrite False`.
- Eval summary does not reflect new command options.
- Metadata mismatch errors mention eval name, model name, reranker name, split, or dataset name.

Safe response:

- Inspect the output directory nesting by embedder and reranker names.
- Use a new `--output_dir` for clean experiments, or ask before setting `--overwrite True`.
- Ensure `--eval_name`, selectors, and model names match existing artifacts when reusing results.
