# Fine-tune Data Formats

FlagEmbedding fine-tuning uses JSONL: one UTF-8 JSON object per line. The same core fields feed embedder and reranker training.

## Core JSONL record

```json
{"query":"question text","pos":["positive passage"],"neg":["negative passage"],"pos_scores":[1.0],"neg_scores":[0.1],"prompt":"optional prompt","type":"normal"}
```

Required fields:

- `query`: non-empty string.
- `pos`: non-empty list of non-empty strings.
- `neg`: list of non-empty strings. Most training commands need negatives; if the source task has none, mine or sample negatives before training.

Optional fields:

- `pos_scores`: numeric list aligned 1:1 with `pos`; required when `--knowledge_distillation True`.
- `neg_scores`: numeric list aligned 1:1 with `neg`; required when `--knowledge_distillation True`.
- `prompt`: prompt text used by prompt-based reranker records and can override default retrieval/rerank instructions in some data flows.
- `type`: ICL embedder task type. Common examples include `normal`, `symmetric_class`, and `symmetric_clustering`; keep values consistent within a dataset family.

## Embedder records

Embedder data trains query-to-passage retrieval. A record must contain `query`, `pos`, and `neg`; optional distillation scores use the same alignment rules. `prompt` may override `query_instruction_for_retrieval`. Decoder-only ICL data can use `type` to select task formatting.

Recommended checks:

- Each positive is a passage that should be close to the query.
- Negatives are plausible but not correct for the query; avoid duplicates of `query` or any `pos` item.
- `train_group_size` should be at most `1 + len(neg)` for every record unless the dataset loader can sample across a directory.
- When `same_dataset_within_batch=True`, each dataset file or directory should contain enough examples for the batch size; configure `small_threshold` and `drop_threshold` deliberately.

## Reranker records

Reranker data trains pairwise scoring from `query` plus each passage in `pos` and `neg`. Required fields are the same. Prompt-based decoder rerankers commonly use `prompt` and query/passage instruction flags so the input resembles `query [sep] passage [sep] prompt`.

Recommended checks:

- For encoder rerankers, keep `query_max_len` and `passage_max_len` conservative enough for pair scoring.
- For decoder rerankers, include query and passage instruction prefixes when the model family expects them.
- For layerwise rerankers, keep model class, `start_layer`, and any cutoff-layer inference plan consistent.

## Knowledge distillation score rules

Use teacher scores only when every record has both aligned score arrays:

- `len(pos_scores) == len(pos)`.
- `len(neg_scores) == len(neg)`.
- Every score is an integer or float, not a string.
- If `--knowledge_distillation False`, score fields may still be present but are not required.
- M3 examples often use `--kd_loss_type m3_kd_loss`; encoder-only baseline examples use `kl_div`.

Run:

```bash
python scripts/validate_finetune_jsonl.py --input train.jsonl --mode embedder --require-negatives --check-scores
```

## Candidate pool for hard negatives

A hard-negative candidate pool is JSONL with one object per line:

```json
{"text":"candidate passage"}
```

Use a candidate pool when the existing `neg` fields are too small or biased. If no candidate pool is supplied, the native mining behavior retrieves from the union of all `pos` and `neg` texts in the training JSONL.

Validate it with:

```bash
python scripts/validate_finetune_jsonl.py --candidate-pool candidates.jsonl
```

## Directory vs file inputs

`--train_data` accepts one or more files or directories. Directories are useful for multiple datasets and for `same_dataset_within_batch`, but they make thresholds important:

- `small_threshold`: datasets smaller than this can be merged.
- `drop_threshold`: merged small datasets below this size can be dropped.
- For tiny smoke tests, set both thresholds to `0` and use very small epoch/batch settings.

## Common invalid cases

- Malformed JSON or blank lines in the middle of a file.
- Missing `query`, `pos`, or `neg`.
- Empty `pos` for any record.
- Empty `neg` when training expects negatives.
- `pos_scores` or `neg_scores` length mismatch.
- Score values encoded as strings.
- ICL `type` omitted or inconsistent for ICL training.
- Prompt-based reranker data without a prompt or without matching command instruction flags.
