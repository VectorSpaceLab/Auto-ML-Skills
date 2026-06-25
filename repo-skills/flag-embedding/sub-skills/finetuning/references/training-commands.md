# Training Commands

FlagEmbedding fine-tuning commands are Python module entry points launched through `torchrun`. Use `scripts/build_finetune_command.py` to generate reviewable commands; it prints only and does not execute.

## Installation and dependency posture

Base inference imports can work without fine-tune extras, but training generally needs:

```bash
pip install 'FlagEmbedding[finetune]'
```

Feature-specific dependencies:

- `--deepspeed ...` requires DeepSpeed installed and a valid JSON config path.
- `--use_flash_attn True` requires flash-attn and a compatible CUDA/PyTorch stack.
- `--bf16` requires hardware/framework bfloat16 support; use `--fp16` on older GPUs if appropriate.
- LoRA options require PEFT-related fine-tune dependencies.

## Command families

| Family | Module | Typical checkpoint | Notes |
| --- | --- | --- | --- |
| Encoder-only embedder | `FlagEmbedding.finetune.embedder.encoder_only.base` | `BAAI/bge-large-en-v1.5` | Baseline retrieval embedding; `sentence_pooling_method=cls`, `kd_loss_type=kl_div`. |
| M3 embedder | `FlagEmbedding.finetune.embedder.encoder_only.m3` | `BAAI/bge-m3` | Multi-function M3; often uses `--unified_finetuning True`, `--use_self_distill True`, `kd_loss_type=m3_kd_loss`. |
| Decoder-only embedder | `FlagEmbedding.finetune.embedder.decoder_only.base` | `BAAI/bge-multilingual-gemma2` | LoRA-heavy; `sentence_pooling_method=last_token`; often uses DeepSpeed stage 1. |
| Decoder-only ICL embedder | `FlagEmbedding.finetune.embedder.decoder_only.icl` | `BAAI/bge-en-icl` | Requires ICL fields/formatting, examples flags, and `same_dataset_within_batch=True`. |
| Encoder-only reranker | `FlagEmbedding.finetune.reranker.encoder_only.base` | `BAAI/bge-reranker-base` | Pairwise reranker baseline; often `knowledge_distillation=True`. |
| Decoder-only reranker | `FlagEmbedding.finetune.reranker.decoder_only.base` | `BAAI/bge-reranker-v2-gemma` | LoRA, decoder model type, optional flash-attn, usually bf16. |
| Decoder layerwise reranker | `FlagEmbedding.finetune.reranker.decoder_only.layerwise` | `BAAI/bge-reranker-v2-minicpm-layerwise` | Adds `start_layer`, `head_multi`, `head_type`, and often `trust_remote_code=True`. |

## Generate a command safely

Minimal encoder-only embedder command:

```bash
python scripts/build_finetune_command.py \
  --family embedder-encoder-base \
  --model-name-or-path BAAI/bge-large-en-v1.5 \
  --train-data data/train.jsonl \
  --output-dir runs/embedder-base \
  --cache-path cache/data \
  --cache-dir cache/model \
  --deepspeed ds_stage0.json \
  --nproc-per-node 2
```

M3 command with self distillation:

```bash
python scripts/build_finetune_command.py \
  --family embedder-m3 \
  --model-name-or-path BAAI/bge-m3 \
  --train-data data/retrieval data/sts.jsonl \
  --output-dir runs/m3 \
  --deepspeed ds_stage0.json \
  --knowledge-distillation true \
  --same-dataset-within-batch true \
  --m3-unified true \
  --m3-self-distill true \
  --kd-loss-type m3_kd_loss
```

Decoder-only embedder command:

```bash
python scripts/build_finetune_command.py \
  --family embedder-decoder-base \
  --model-name-or-path BAAI/bge-multilingual-gemma2 \
  --train-data data/train.jsonl \
  --output-dir runs/decoder-embedder \
  --deepspeed ds_stage1.json \
  --precision fp16 \
  --use-lora true \
  --target-modules q_proj k_proj v_proj o_proj gate_proj down_proj up_proj \
  --sentence-pooling-method last_token
```

ICL embedder command:

```bash
python scripts/build_finetune_command.py \
  --family embedder-decoder-icl \
  --model-name-or-path BAAI/bge-en-icl \
  --train-data data/icl \
  --output-dir runs/icl \
  --deepspeed ds_stage1.json \
  --same-dataset-within-batch true \
  --retrieval-use-examples true \
  --query-max-len 2048 \
  --example-query-max-len 256 \
  --example-passage-max-len 256
```

Encoder reranker command:

```bash
python scripts/build_finetune_command.py \
  --family reranker-encoder-base \
  --model-name-or-path BAAI/bge-reranker-base \
  --train-data data/reranker.jsonl \
  --output-dir runs/reranker-base \
  --knowledge-distillation true \
  --learning-rate 6e-5
```

Decoder reranker command:

```bash
python scripts/build_finetune_command.py \
  --family reranker-decoder-base \
  --model-name-or-path BAAI/bge-reranker-v2-gemma \
  --train-data data/prompt-reranker.jsonl \
  --output-dir runs/reranker-decoder \
  --precision bf16 \
  --use-lora true \
  --use-flash-attn true \
  --query-instruction-for-rerank 'A: ' \
  --passage-instruction-for-rerank 'B: '
```

Layerwise reranker command:

```bash
python scripts/build_finetune_command.py \
  --family reranker-decoder-layerwise \
  --model-name-or-path BAAI/bge-reranker-v2-minicpm-layerwise \
  --train-data data/prompt-reranker.jsonl \
  --output-dir runs/reranker-layerwise \
  --precision bf16 \
  --use-lora true \
  --use-flash-attn true \
  --trust-remote-code true \
  --start-layer 8 \
  --head-multi true \
  --head-type simple
```

## DeepSpeed config choices

FlagEmbedding examples use two simple config families:

- Stage 0: good starting point for encoder-only embedder/reranker and many M3 jobs.
- Stage 1: common for larger decoder-only embedder jobs.

The builder accepts any `--deepspeed` path but does not create the config. Verify that the JSON file exists in the working project before running the printed command. Do not hard-code paths from a generated skill or source checkout into commands.

## Important flags by concern

Data and batching:

- `--train_data`: one or more files/directories.
- `--cache_path`: tokenized data cache location.
- `--train_group_size`: one query plus positives/negatives group size.
- `--same_dataset_within_batch True`: keep batches from the same dataset; combine with thresholds intentionally.
- `--small_threshold` and `--drop_threshold`: control merging/dropping tiny datasets.

Memory and speed:

- `--per_device_train_batch_size`, `--gradient_accumulation_steps`, and `--sub_batch_size` control memory pressure.
- `--gradient_checkpointing` reduces memory at speed cost.
- `--negatives_cross_device` increases contrastive negatives but requires distributed communication and memory.
- `--fp16` or `--bf16` should match hardware support; do not enable both.

Embedder-specific:

- `--query_instruction_for_retrieval` and `--query_instruction_format` format queries.
- `--sentence_pooling_method cls|mean|last_token` must match model family.
- `--normalize_embeddings True` is common for retrieval embeddings.
- `--kd_loss_type kl_div|m3_kd_loss` should match model family and score usage.

Reranker-specific:

- `--query_instruction_for_rerank`, `--passage_instruction_for_rerank`, and formats shape pair inputs.
- `--model_type decoder` is needed for decoder reranker families.
- Layerwise rerankers add `--start_layer`, `--head_multi`, and `--head_type`.

LoRA and decoder models:

- `--use_lora True` plus `--lora_rank`, `--lora_alpha`, and `--target_modules` is common for decoder-only families.
- `--save_merged_lora_model True` saves a merged model after training when supported.
- `--additional_special_tokens` is used by decoder embedders and ICL workflows.

## Before executing a printed command

- Validate every train file with `scripts/validate_finetune_jsonl.py`.
- Confirm optional dependencies for selected flags.
- Confirm `output_dir` overwrite policy; remove `--overwrite_output_dir` if accidental overwrite is risky.
- Confirm model/cache paths and credentials for private checkpoints.
- Start with a tiny fixture and low `--max_steps` or small epoch if the user wants a smoke test.
