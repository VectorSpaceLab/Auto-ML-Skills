---
name: data-preparation
description: "Helps agents prepare FlagEmbedding retrieval data with JSONL validation, hard-negative mining, reranker teacher scores, and length bucketing."
disable-model-invocation: true
---

# FlagEmbedding Data Preparation

Use this sub-skill when the user needs to validate training JSONL, mine hard negatives, add reranker teacher scores, split examples by token length, or prepare retrieval data for fine-tuning/evaluation.

## Workflows

Read [references/workflows.md](references/workflows.md) for commands and parameter notes for:

| Workflow | Script |
| --- | --- |
| Validate train JSONL | `scripts/validate_retrieval_jsonl.py` |
| Mine hard negatives | `scripts/hn_mine.py` |
| Add reranker scores | `scripts/add_reranker_score.py` |
| Split by token length | `scripts/split_data_by_length.py` |

These scripts are bundled self-contained adaptations of the repository helper scripts. They do not require the original repository checkout.

## Validate First

For training data:

```bash
python scripts/validate_retrieval_jsonl.py --input train.jsonl --mode train
```

For distillation data:

```bash
python scripts/validate_retrieval_jsonl.py --input train_scored.jsonl --mode train --require-scores
```

## Hard-Negative Mining

Hard-negative mining downloads/loads an embedder and uses FAISS. Run it only after model downloads and compute resources are acceptable:

```bash
python scripts/hn_mine.py \
  --input_file train.jsonl \
  --output_file train_mined.jsonl \
  --range_for_sampling 2-200 \
  --negative_number 15 \
  --embedder_name_or_path BAAI/bge-base-en-v1.5 \
  --use_fp16 True
```

Use `--candidate_pool pool.jsonl` when negatives should come from an external corpus. Candidate pool rows must contain a `text` field.

## Teacher Scores

Add reranker scores for distillation:

```bash
python scripts/add_reranker_score.py \
  --input_file train_mined.jsonl \
  --output_file train_scored.jsonl \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --reranker_max_length 512
```

Then train with `--knowledge_distillation True`.

## Length Bucketing

Split long training rows by token length:

```bash
python scripts/split_data_by_length.py \
  --input_path train_scored.jsonl \
  --output_dir train_split \
  --model_name_or_path BAAI/bge-m3 \
  --length_list 0 500 1000 2000 3000 4000 5000 6000 7000 \
  --num_proc 4
```

## References

Read [references/workflows.md](references/workflows.md) for full parameter notes and when to use each preprocessing step.

Read [references/data-formats.md](references/data-formats.md) for JSONL schemas for training rows, candidate pools, scored rows, and split outputs.

Read [references/troubleshooting.md](references/troubleshooting.md) for FAISS, candidate-pool, score-length, tokenizer, and overwrite issues.
