# Utility Scripts for Fine-tuning Data

FlagEmbedding provides three important preprocessing utilities: hard-negative mining, teacher-score generation, and length-based splitting. This sub-skill bundles safe validators/builders and a no-ML length splitter. Mining and teacher scoring are intentionally documented as commands to review because they perform model inference and may download checkpoints.

## Hard-negative mining

Purpose: retrieve candidate passages for each query and sample hard negatives from a top-k range while excluding positives and the query text.

Native behavior to preserve conceptually:

- Input: fine-tune JSONL with `query`, `pos`, and optional existing `neg`.
- Candidate source: explicit candidate pool JSONL with `text`, or the union of all `pos` and `neg` texts in the input.
- Retrieval: embed corpus and queries with `FlagAutoModel.from_finetuned`, then search with FAISS.
- Sampling: `range_for_sampling` like `2-200` samples from ranked results; larger left bounds make negatives easier.
- Output: same JSONL records with `neg` replaced or filled.

Reviewable command shape for an approved mining utility in the user's environment:

```bash
python <hard-negative-mining-script> \
  --input_file train.jsonl \
  --output_file train.mined.jsonl \
  --range_for_sampling 2-200 \
  --negative_number 15 \
  --embedder_name_or_path BAAI/bge-base-en-v1.5 \
  --embedder_model_class encoder-only-base \
  --normalize_embeddings True \
  --pooling_method cls \
  --search_batch_size 64
```

This skill intentionally does not bundle a model-running miner; use the template only after the user approves inference cost and supplies or installs the utility.

Optional arguments:

- `--candidate_pool candidates.jsonl`: each line must be `{"text":"..."}`.
- `--use_gpu_for_searching`: use FAISS GPU; requires a compatible FAISS GPU install.
- `--devices cuda:0 cuda:1`: devices for embedding inference.
- `--query_instruction_for_retrieval` and `--query_instruction_format_for_retrieval`: align mining with the target embedder family.
- `--examples_for_task` and `--examples_instruction_format`: only for decoder-only ICL mining.
- `--trust_remote_code True`: only when the model requires it and the user accepts the risk.
- `--cache_dir`: local model cache.
- `--embedder_query_max_length`, `--embedder_passage_max_length`, `--batch_size`: inference sizing.

Safety checks before running mining:

- Validate input and candidate pool with `scripts/validate_finetune_jsonl.py`.
- Ensure `negative_number` is feasible for the candidate pool size.
- Ensure `range_for_sampling` is `start-end` with `0 <= start < end`; use `2-200` or `10-210` as typical starting ranges.
- Decide CPU vs GPU FAISS explicitly; CPU is slower but avoids GPU FAISS install issues.
- Warn that checkpoint downloads and expensive inference can occur.

## Reranker teacher-score generation

Purpose: add `pos_scores` and `neg_scores` for knowledge distillation by scoring every `(query, passage)` pair with a reranker.

Native behavior to preserve conceptually:

- Input: JSONL with `query`, `pos`, and `neg`.
- Pairs: all positives first, then all negatives per record.
- Model: `FlagAutoReranker.from_finetuned`.
- Output: original records plus aligned `pos_scores` and `neg_scores` numeric lists.

Reviewable command shape for an approved teacher-scoring utility in the user's environment:

```bash
python <reranker-score-script> \
  --input_file train.mined.jsonl \
  --output_file train.scored.jsonl \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --reranker_model_class encoder-only-base \
  --reranker_query_max_length 512 \
  --reranker_max_length 1024 \
  --reranker_batch_size 3000
```

This skill intentionally does not bundle a model-running scorer; use the template only after the user approves inference cost and supplies or installs the utility.

Optional arguments:

- `--devices cuda:0 cuda:1`: inference devices.
- `--use_fp16 True` or `--use_bf16 True`: precision for teacher inference.
- `--reranker_peft_path`: adapter path.
- `--query_instruction_for_rerank`, `--passage_instruction_for_rerank`, and formats: pair formatting.
- `--normalize True`: normalize scores if desired.
- `--prompt`: reranker prompt.
- `--cutoff_layers`, `--compress_ratio`, `--compress_layers`: layerwise/lightweight reranker options.

Safety checks before scoring:

- Validate `query`, `pos`, and `neg`; every record should have at least one positive and enough negatives.
- Estimate pair count as `sum(len(pos)+len(neg))`; teacher scoring cost scales with this total.
- Use smaller batch sizes if GPU memory is limited.
- After scoring, run `scripts/validate_finetune_jsonl.py --check-scores`.

## Split data by length

Purpose: split JSONL into length buckets so long examples can be trained separately or assigned lower batch sizes.

Bundled safe splitter:

```bash
python scripts/split_data_by_length.py \
  --input-path train.jsonl \
  --output-dir train_split \
  --length-list 0 500 1000 2000 3000 4000 5000 6000 7000 \
  --length-mode chars
```

Defaults are safe:

- No FlagEmbedding, torch, datasets, transformers, or tokenizer import is required.
- `--length-mode chars` estimates length by Unicode character count over `query`, `pos`, and `neg`.
- `--length-mode whitespace-tokens` estimates by whitespace token count.
- `--length-mode hf-tokenizer` is opt-in and can download a tokenizer through `transformers.AutoTokenizer.from_pretrained`; use only after user approval.

Output behavior:

- Input can be one JSONL file or a directory of JSONL files.
- Files are written as `<stem>_len-<left>-<right>.jsonl`; final bucket uses `inf`.
- A JSONL log is written to the output directory.
- Existing bucket files are skipped unless `--overwrite` is passed.

When to split:

- Decoder-only embedder or reranker jobs have high memory variance from long passages.
- `query_max_len`, `passage_max_len`, or ICL example lengths differ across datasets.
- You need separate commands with smaller `per_device_train_batch_size` for long buckets.

## Utility ordering

Common preparation pipeline:

1. Validate raw JSONL schema.
2. Mine hard negatives if negatives are weak or absent.
3. Add reranker teacher scores if using knowledge distillation.
4. Validate scored JSONL with score alignment.
5. Split by length if memory variance is high.
6. Build training command from the final file/directory list.

Do not treat native utility commands as runtime dependencies of this skill. They are behavior references and command templates; future agents should adapt them to the user's installed environment and explicit execution approval.
