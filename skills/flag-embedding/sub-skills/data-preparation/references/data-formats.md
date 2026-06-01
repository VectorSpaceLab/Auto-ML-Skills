# Data Preparation Formats

Read this when creating files for hard-negative mining, teacher scoring, or length splitting.

## Training JSONL

Required shape:

```json
{"query": "query text", "pos": ["positive text"], "neg": ["negative text"]}
```

Optional distillation fields:

```json
{"pos_scores": [2.4], "neg_scores": [-0.8]}
```

Optional prompt/ICL fields:

```json
{"prompt": "task prompt", "type": "normal"}
```

`pos_scores` length must equal `pos` length. `neg_scores` length must equal `neg` length.

## Candidate Pool JSONL

Hard-negative mining accepts an optional candidate pool file:

```json
{"text": "candidate passage text"}
```

The helper uses unique candidate text strings. If no candidate pool is provided, it builds a corpus from all `pos` and existing `neg` values in the input training data.

## Hard-Negative Output

The hard-negative mining output preserves each original row and replaces or fills `neg` with sampled negatives:

```json
{"query": "query text", "pos": ["positive text"], "neg": ["mined hard negative", "..."]}
```

It excludes positives and query text when sampling from nearest neighbors. If not enough nearest neighbors remain, it samples fallback negatives from the corpus.

## Reranker Score Output

The teacher-score script adds:

```json
{
  "query": "query text",
  "pos": ["positive text"],
  "neg": ["negative text"],
  "pos_scores": [5.2],
  "neg_scores": [-4.1]
}
```

The score order follows all positives first, then all negatives for each row.

## Length-Split Output

The length splitter writes files named like:

```text
<input-stem>_len-0-500.jsonl
<input-stem>_len-500-1000.jsonl
...
```

It also appends JSON log entries to the configured log file in `output_dir`.
