---
name: finetuning
description: "Helps agents fine-tune FlagEmbedding embedders and rerankers with torchrun, DeepSpeed, LoRA, and retrieval JSONL data."
disable-model-invocation: true
---

# FlagEmbedding Fine-Tuning

Use this sub-skill when the user wants to train or fine-tune a FlagEmbedding embedder or reranker, prepare training commands, choose training modules, validate JSONL train data, add distillation scores, or configure DeepSpeed.

## Install

Fine-tuning needs the extra dependencies:

```bash
python -m pip install -U "FlagEmbedding[finetune]"
```

If `flash-attn` or `deepspeed` installation fails, resolve the target Torch/CUDA compatibility first. For CPU-only or inference-only work, do not install the fine-tuning extra unnecessarily.

## Choose The Training Module

Use these module entry points with `torchrun`:

| Workflow | Module |
| --- | --- |
| Encoder-only embedder | `FlagEmbedding.finetune.embedder.encoder_only.base` |
| BGE-M3 embedder | `FlagEmbedding.finetune.embedder.encoder_only.m3` |
| Decoder-only/LLM embedder | `FlagEmbedding.finetune.embedder.decoder_only.base` |
| ICL decoder-only embedder | `FlagEmbedding.finetune.embedder.decoder_only.icl` |
| Encoder-only reranker | `FlagEmbedding.finetune.reranker.encoder_only.base` |
| Decoder-only/LLM reranker | `FlagEmbedding.finetune.reranker.decoder_only.base` |
| Layerwise decoder-only reranker | `FlagEmbedding.finetune.reranker.decoder_only.layerwise` |

Read [references/training-workflows.md](references/training-workflows.md) for command templates adapted from the repository examples.

## Validate Data First

Training data is JSONL. Each row must include:

```json
{"query": "text", "pos": ["positive text"], "neg": ["negative text"]}
```

Distillation rows add `pos_scores` and `neg_scores` with matching lengths. Embedder ICL data may add `type`; prompt-based reranker data may add `prompt`.

Read [references/data-formats.md](references/data-formats.md) for schemas and examples. Run the bundled validator:

```bash
python ../data-preparation/scripts/validate_retrieval_jsonl.py --input train.jsonl --mode train
```

From this sub-skill directory, the same script is linked through the data-preparation sub-skill rather than duplicated.

## Build Configs

The original examples use DeepSpeed stage 0 or stage 1 config files. This skill bundles a generator:

```bash
python scripts/write_deepspeed_config.py --stage 0 --output ds_stage0.json
python scripts/write_deepspeed_config.py --stage 1 --output ds_stage1.json
```

Then pass `--deepspeed ./ds_stage0.json` or `--deepspeed ./ds_stage1.json`.

## Command Construction Pattern

Start from a small run, then scale:

```bash
export WANDB_MODE=disabled
torchrun --nproc_per_node 1 \
  -m FlagEmbedding.finetune.embedder.encoder_only.base \
  --model_name_or_path BAAI/bge-base-en-v1.5 \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --query_instruction_for_retrieval "Represent this sentence for searching relevant passages: " \
  --query_instruction_format "{}{}" \
  --knowledge_distillation False \
  --output_dir ./outputs/bge-base-ft \
  --overwrite_output_dir \
  --learning_rate 1e-5 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --dataloader_drop_last True \
  --logging_steps 10 \
  --save_steps 500 \
  --sentence_pooling_method cls \
  --normalize_embeddings True
```

## References

Read [references/training-workflows.md](references/training-workflows.md) for embedder, M3, decoder-only, ICL, reranker, LoRA, layerwise, and DeepSpeed command templates.

Read [references/data-formats.md](references/data-formats.md) for JSONL row schemas, distillation score fields, prompt fields, and dataset directory behavior.

Read [references/arguments.md](references/arguments.md) for important verified argument groups and defaults.

Read [references/troubleshooting.md](references/troubleshooting.md) for common training failures: missing negatives, distillation length mismatch, DeepSpeed config paths, CUDA OOM, LoRA target modules, and `trust_remote_code`.

## Scripts

Run [scripts/write_deepspeed_config.py](scripts/write_deepspeed_config.py) to create a reusable DeepSpeed config in the current project.

Read or adapt [scripts/build_training_command.py](scripts/build_training_command.py) to construct a conservative `torchrun` command for a selected workflow.

Use the data-preparation sub-skill scripts for hard-negative mining, reranker teacher scoring, and train JSONL validation.
