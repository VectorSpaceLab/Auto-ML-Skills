---
name: finetuning
description: "Use for FlagEmbedding embedder or reranker fine-tuning, JSONL train-data format, hard-negative mining, teacher-score generation, torchrun commands, LoRA, deepspeed, and training troubleshooting."
---

# FlagEmbedding Finetuning

Use this sub-skill when the user wants to fine-tune a BGE embedder or reranker, prepare retrieval training data, mine hard negatives, add teacher scores, choose train modules, validate JSONL data, or debug training failures.

## Install

Fine-tuning uses optional dependencies:

```bash
python -m pip install -U "FlagEmbedding[finetune]"
```

The `finetune` extra includes `deepspeed` and `flash-attn`. These are sensitive to torch, CUDA, compiler, and Python versions. If the user only needs data validation or CPU-side planning, do not install or compile heavy CUDA extras until needed.

## Read These First

- `references/data-formats.md` for embedder/reranker train JSONL schemas, score fields, prompts, and examples.
- `references/training-workflows.md` for torchrun module names, standard embedder/reranker recipes, M3, decoder-only, ICL, LoRA, hard-negative mining, teacher scores, and split-by-length workflows.
- `references/troubleshooting.md` for missing data, optional dependency, CUDA, deepspeed, flash-attn, OOM, and output-checkpoint issues.

Run:

- `scripts/validate_finetune_jsonl.py` before training, hard-negative mining, or teacher scoring.
- `scripts/add_reranker_scores.py` when the user asks to add teacher scores with a reranker. This loads a model and can download checkpoints.
- `scripts/mine_hard_negatives.py` when the user asks to mine negatives. This loads an embedder and requires FAISS.
- `scripts/split_by_length.py` when the user asks to bucket training rows by token length. This loads a tokenizer and can download it.

## Training Data Basics

Each JSONL row must contain:

```json
{"query": "question text", "pos": ["positive passage"], "neg": ["negative passage"]}
```

Optional fields:

- `pos_scores` and `neg_scores` for knowledge distillation.
- `prompt` for query/reranker prompt handling.
- `type` for `bge-en-icl` style embedder fine-tuning.

Validate a file:

```bash
python scripts/validate_finetune_jsonl.py train.jsonl --task embedder
python scripts/validate_finetune_jsonl.py train.jsonl --task reranker --require-scores
```

## Choose A Training Module

Embedder modules:

- `FlagEmbedding.finetune.embedder.encoder_only.base`: standard encoder-only embedder.
- `FlagEmbedding.finetune.embedder.encoder_only.m3`: BGE-M3/unified fine-tuning.
- `FlagEmbedding.finetune.embedder.decoder_only.base`: decoder-only embedding models with optional LoRA.
- `FlagEmbedding.finetune.embedder.decoder_only.icl`: ICL embedding models.

Reranker modules:

- `FlagEmbedding.finetune.reranker.encoder_only.base`: encoder-only rerankers.
- `FlagEmbedding.finetune.reranker.decoder_only.base`: decoder-only LLM rerankers.
- `FlagEmbedding.finetune.reranker.decoder_only.layerwise`: layerwise LLM rerankers.

## Minimal Encoder Embedder Command Shape

```bash
torchrun --nproc_per_node 1 \
  -m FlagEmbedding.finetune.embedder.encoder_only.base \
  --model_name_or_path BAAI/bge-base-en-v1.5 \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --output_dir ./outputs/bge-base-finetuned \
  --overwrite_output_dir \
  --learning_rate 1e-5 \
  --fp16 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --dataloader_drop_last True \
  --logging_steps 10 \
  --save_steps 1000 \
  --sentence_pooling_method cls \
  --normalize_embeddings True
```

Add `--deepspeed path/to/ds_stage0.json` only when the environment is ready for deepspeed and the user wants it.

## Minimal Encoder Reranker Command Shape

```bash
torchrun --nproc_per_node 1 \
  -m FlagEmbedding.finetune.reranker.encoder_only.base \
  --model_name_or_path BAAI/bge-reranker-v2-m3 \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --output_dir ./outputs/reranker-finetuned \
  --overwrite_output_dir \
  --learning_rate 6e-5 \
  --fp16 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 1 \
  --logging_steps 10 \
  --save_steps 1000
```

## Data Preparation Helpers

Hard-negative mining, teacher scoring, and length bucketing are side-effectful and may download models, use GPUs, or write new files. Do not run them unless the user requested them.

Hard negatives:

```bash
python scripts/mine_hard_negatives.py \
  --input_file train.jsonl \
  --output_file train_minedHN.jsonl \
  --range_for_sampling 2-200 \
  --negative_number 15 \
  --embedder_name_or_path BAAI/bge-base-en-v1.5
```

Teacher scores:

```bash
python scripts/add_reranker_scores.py \
  --input_file train_minedHN.jsonl \
  --output_file train_score.jsonl \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3
```

Split by length:

```bash
python scripts/split_by_length.py \
  --input_path train_data \
  --output_dir train_data_split \
  --model_name_or_path BAAI/bge-m3
```
