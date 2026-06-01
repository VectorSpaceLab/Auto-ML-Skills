# Evaluation Data Formats

Read this when creating a custom retrieval dataset for `FlagEmbedding.evaluation.custom` or validating benchmark cache inputs.

## Custom Retrieval Layout

A dataset directory must contain:

```text
corpus.jsonl
<split>_queries.jsonl
<split>_qrels.jsonl
```

For multiple datasets, `dataset_dir` may contain child directories, each with the same three-file layout.

## Corpus File

Recommended JSONL shape:

```json
{"id": "doc1", "text": "document text"}
```

Some loaders also accept fields such as `title`; keep `id` unique and text content non-empty.

## Queries File

Recommended JSONL shape:

```json
{"id": "q1", "text": "query text"}
```

The split prefix in the filename must match `--splits`. For `--splits dev test`, provide `dev_queries.jsonl`, `dev_qrels.jsonl`, `test_queries.jsonl`, and `test_qrels.jsonl`.

## Qrels File

Recommended JSONL shape:

```json
{"qid": "q1", "docid": "doc1", "relevance": 1}
```

Use integer relevance values when possible. Every `qid` should exist in the queries file. Every `docid` should exist in the corpus file.

## Validation

Run:

```bash
python sub-skills/evaluation/scripts/check_eval_dataset.py --dataset-dir ./eval_data --splits test
```

The bundled script checks required files and common id consistency for simple JSONL schemas.

## Output Files

Evaluation commands commonly write:

```text
search result files under --output_dir
optional corpus embeddings under --corpus_embd_save_dir
aggregate metrics at --eval_output_path
```

Use `--overwrite True` only when replacing existing results is intended.
