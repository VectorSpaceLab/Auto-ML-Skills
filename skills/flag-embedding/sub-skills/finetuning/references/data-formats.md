# Fine-Tuning Data Formats

Read this before creating or validating FlagEmbedding training datasets.

## Base Training JSONL

Training data is line-delimited JSON. Each row must include:

```json
{"query": "query text", "pos": ["positive passage"], "neg": ["negative passage"]}
```

`query` is a string. `pos` is a list of positive texts. `neg` is a list of negative texts. If a source dataset has no negatives, mine hard negatives or sample negatives from a corpus before training.

Rows can live in a single `.jsonl` file or in a directory containing multiple `.jsonl` files. The `--train_data` argument accepts one or more files/directories.

## Knowledge Distillation Fields

For distillation, include:

```json
{
  "query": "query text",
  "pos": ["positive passage"],
  "neg": ["negative passage"],
  "pos_scores": [4.2],
  "neg_scores": [-1.3]
}
```

`len(pos_scores)` must equal `len(pos)`. `len(neg_scores)` must equal `len(neg)`. Set `--knowledge_distillation True` only when these fields are present and valid.

Use the data-preparation sub-skill's reranker scoring workflow to generate these fields.

## Prompt And ICL Fields

Embedder rows may include:

```json
{"prompt": "instruction text", "type": "normal"}
```

`prompt` covers or overrides query instruction behavior for that example. `type` is used by ICL workflows and may include values such as `normal`, `symmetric_class`, or `symmetric_clustering`.

Prompt-based reranker rows may include:

```json
{"prompt": "Given a query A and passage B, determine whether B answers A."}
```

The decoder reranker input format combines query, passage, and prompt according to query/passage instruction settings.

## Practical Dataset Checks

Before training, verify:

```text
Every line is valid JSON.
Every row has query, pos, and neg.
query is a non-empty string.
pos and neg are non-empty lists of strings.
No distillation score list length mismatch exists.
For ICL workflows, type/prompt conventions match the intended runner.
```

Run:

```bash
python sub-skills/data-preparation/scripts/validate_retrieval_jsonl.py --input train.jsonl --mode train
```

## Hard Negatives

Hard-negative mining retrieves candidate passages for each query and samples negatives from a rank range, excluding positives and the query text. The source helper defaults to a range such as `10-210`; examples use `2-200` for harder negatives.

If negatives are too difficult, sample from a later rank range, such as `60-300`. If negatives are too easy, sample from earlier ranks.

## Length Bucketing

Long-sequence training benefits from splitting rows by maximum token length across query, positives, and negatives. Use the data-preparation sub-skill's length-splitting script for this workflow.
