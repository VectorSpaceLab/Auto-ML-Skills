# Evaluation Troubleshooting

Read this when FlagEmbedding benchmark or custom evaluation commands fail.

## Missing Dependencies

Install only the benchmark extras needed:

- MTEB: `mteb`.
- BEIR: `beir`.
- AIR-Bench: `air-benchmark`.
- Metrics: `pytrec_eval`; if it fails to build/install, try `pytrec-eval-terrier`.
- Retrieval index: FAISS CPU/GPU wheel matched to Python, CUDA, and platform.

Run a help command before a long evaluation:

```bash
python -m FlagEmbedding.evaluation.beir --help
```

## Custom Dataset Errors

Validate first:

```bash
python scripts/validate_custom_eval_dataset.py ./my_eval --splits test
```

Common issues:

- Missing `corpus.jsonl`.
- Split mismatch, for example command uses `--splits dev` but only `test_queries.jsonl` exists.
- Query or corpus ids use inconsistent key names.
- Qrels reference ids missing from corpus or query files.
- JSONL files contain arrays instead of one JSON object per line.

## Stale Outputs

If results look unchanged:

- Check `--output_dir`.
- Check `--eval_output_path`.
- Set `--overwrite True` only when the user wants to replace existing outputs.
- Clear or change `--corpus_embd_save_dir` if old corpus embeddings should not be reused.

## Dataset Downloads And Caches

`--dataset_dir` can be a download target for supported benchmarks or a required local path for custom data. `--cache_path` controls dataset cache. `--cache_dir` controls model cache.

Use `--force_redownload True` only when the user wants to refresh downloaded datasets.

## Reranker Issues

If reranking fails:

- First run retrieval without `--reranker_name_or_path` to isolate embedder/index problems.
- Verify `--reranker_model_class` for custom rerankers.
- Reduce `--rerank_top_k` and `--reranker_batch_size`.
- Check `--reranker_query_max_length` and `--reranker_max_length`.

## Metric Or Output Method Errors

Use `--eval_output_method json` or `markdown`. MTEB official output may be JSON-oriented. Keep metric names aligned with the benchmark; common retrieval metrics include `ndcg_at_10`, `recall_at_100`, and MKQA-style `qa_recall_at_20`.
