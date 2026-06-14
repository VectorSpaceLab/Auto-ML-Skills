# Evaluation Data Formats

Read this when preparing custom FlagEmbedding retrieval evaluation data.

## Single Dataset Layout

```text
dataset_dir/
  corpus.jsonl
  test_queries.jsonl
  test_qrels.jsonl
```

For a different split, replace `test` with the split name:

```text
dev_queries.jsonl
dev_qrels.jsonl
```

## Multiple Dataset Layout

`dataset_dir` may contain multiple dataset subdirectories, each with the same required files:

```text
dataset_dir/
  dataset_a/
    corpus.jsonl
    test_queries.jsonl
    test_qrels.jsonl
  dataset_b/
    corpus.jsonl
    test_queries.jsonl
    test_qrels.jsonl
```

Use `--dataset_names dataset_a dataset_b` when evaluating selected subdirectories.

## JSONL Shapes

`corpus.jsonl` should have one document per line. Common accepted keys are:

```json
{"id": "doc1", "text": "document text"}
{"_id": "doc2", "title": "optional title", "text": "document text"}
```

`<split>_queries.jsonl` should have one query per line:

```json
{"id": "q1", "text": "query text"}
{"_id": "q2", "text": "another query"}
```

`<split>_qrels.jsonl` should map queries to relevant documents. Common accepted shapes:

```json
{"query-id": "q1", "corpus-id": "doc1", "score": 1}
{"qid": "q1", "docid": "doc2", "relevance": 1}
{"query_id": "q1", "doc_id": "doc3", "score": 1}
```

Because loader expectations can vary by benchmark integration, keep ids as strings and use the most explicit key names possible.

## Validation

Run:

```bash
python scripts/validate_custom_eval_dataset.py ./my_eval --splits test
```

The validator checks required files, JSONL parseability, id/text presence, qrel references, and empty files. It is conservative and self-contained.
