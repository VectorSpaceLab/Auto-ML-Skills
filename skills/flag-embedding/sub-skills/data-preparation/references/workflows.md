# Data Preparation Workflows

Read this for FlagEmbedding helper workflows adapted from the repository scripts.

## Validate Training Data

```bash
python scripts/validate_retrieval_jsonl.py --input train.jsonl --mode train
```

For scored distillation data:

```bash
python scripts/validate_retrieval_jsonl.py --input train_scored.jsonl --mode train --require-scores
```

Run validation before hard-negative mining, teacher scoring, and training.

## Mine Hard Negatives

```bash
python scripts/hn_mine.py \
  --input_file train.jsonl \
  --output_file train_minedHN.jsonl \
  --range_for_sampling 2-200 \
  --negative_number 15 \
  --embedder_name_or_path BAAI/bge-base-en-v1.5 \
  --embedder_batch_size 128 \
  --embedder_query_max_length 512 \
  --embedder_passage_max_length 512 \
  --use_fp16 True
```

Important parameters:

| Parameter | Meaning |
| --- | --- |
| `--input_file` | Training JSONL with `query`, `pos`, and optional `neg` |
| `--output_file` | Output JSONL with mined `neg` |
| `--candidate_pool` | Optional JSONL with `text` field |
| `--range_for_sampling` | Rank range, e.g. `2-200` or `60-300` |
| `--negative_number` | Number of negatives to sample per query |
| `--use_gpu_for_searching` | Use FAISS GPU index |
| `--search_batch_size` | FAISS search batch size |
| `--embedder_name_or_path` | Embedder model or path |
| `--embedder_model_class` | Required for custom/unmapped embedders |
| `--pooling_method` | Pooling override |
| `--query_instruction_for_retrieval` | Query instruction |
| `--query_instruction_format_for_retrieval` | Query instruction format |
| `--trust_remote_code` | Allow remote model code |
| `--cache_dir` | Model cache |

Sampling later ranks makes negatives easier. Sampling earlier ranks makes negatives harder but can introduce false negatives.

## Add Reranker Teacher Scores

```bash
python scripts/add_reranker_score.py \
  --input_file train_minedHN.jsonl \
  --output_file train_score.jsonl \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --reranker_batch_size 256 \
  --reranker_max_length 512 \
  --use_fp16 True
```

Important parameters:

| Parameter | Meaning |
| --- | --- |
| `--input_file` | JSONL with `query`, `pos`, and `neg` |
| `--output_file` | JSONL with `pos_scores` and `neg_scores` added |
| `--reranker_name_or_path` | Reranker model or path |
| `--reranker_model_class` | Required for custom/unmapped rerankers |
| `--reranker_peft_path` | PEFT adapter path |
| `--reranker_query_max_length` | Query max length |
| `--reranker_max_length` | Total max length |
| `--normalize` | Apply sigmoid to scores |
| `--cutoff_layers` | Layerwise/lightweight reranker layers |
| `--compress_ratio` | Lightweight reranker compression ratio |
| `--compress_layers` | Lightweight reranker compression layers |

Use raw scores for distillation unless a specific workflow requires normalized scores.

## Split Data By Length

```bash
python scripts/split_data_by_length.py \
  --input_path train_score.jsonl \
  --output_dir train_split \
  --cache_dir ./cache/data \
  --log_name .split_log \
  --length_list 0 500 1000 2000 3000 4000 5000 6000 7000 \
  --model_name_or_path BAAI/bge-m3 \
  --num_proc 16
```

The splitter tokenizes `query`, all positives, and all negatives, computes the maximum token length in each row, and writes rows into length range files.

Use this before long-context training or when grouping similar lengths helps memory usage.
