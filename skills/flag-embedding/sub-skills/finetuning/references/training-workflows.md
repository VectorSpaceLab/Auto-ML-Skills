# Training Workflows

Read this for concrete command shapes and decision points for FlagEmbedding fine-tuning.

## Common Arguments

Common model/data flags:

- `--model_name_or_path`: initial model checkpoint.
- `--config_name`, `--tokenizer_name`: override config/tokenizer if different.
- `--cache_dir`: model cache.
- `--trust_remote_code`: execute custom model code when required.
- `--token`: Hugging Face token; defaults to `HF_TOKEN` in the environment.
- `--train_data`: one or more JSONL files or directories.
- `--cache_path`: cached preprocessed data.
- `--train_group_size`: group size for query positives/negatives.
- `--query_max_len`, `--passage_max_len`, `--max_len`: token truncation lengths.
- `--pad_to_multiple_of`: padding multiple, often `8`.
- `--knowledge_distillation`: requires `pos_scores` and `neg_scores`.
- `--query_instruction_*`, `--passage_instruction_*`: instruction strings and formats.
- Standard Hugging Face `TrainingArguments`: `--output_dir`, `--learning_rate`, `--fp16`, `--bf16`, `--num_train_epochs`, `--per_device_train_batch_size`, `--gradient_accumulation_steps`, `--warmup_ratio`, `--logging_steps`, `--save_steps`.

## Encoder-Only Embedder

Module:

```bash
python -m FlagEmbedding.finetune.embedder.encoder_only.base --help
```

Typical command:

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.encoder_only.base \
  --model_name_or_path BAAI/bge-large-en-v1.5 \
  --cache_dir ./cache/model \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --query_instruction_for_retrieval "Represent this sentence for searching relevant passages: " \
  --query_instruction_format "{}{}" \
  --knowledge_distillation False \
  --output_dir ./outputs/embedder-base \
  --overwrite_output_dir \
  --learning_rate 1e-5 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --logging_steps 10 \
  --save_steps 1000 \
  --negatives_cross_device \
  --temperature 0.02 \
  --sentence_pooling_method cls \
  --normalize_embeddings True \
  --kd_loss_type kl_div
```

## BGE-M3 Embedder

Module:

```bash
python -m FlagEmbedding.finetune.embedder.encoder_only.m3 --help
```

Use `--kd_loss_type m3_kd_loss` for M3 knowledge distillation. Additional M3 arguments include:

- `--colbert_dim`
- `--unified_finetuning`
- `--use_self_distill`
- `--fix_encoder`
- `--self_distill_start_step`

Command shape:

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.encoder_only.m3 \
  --model_name_or_path BAAI/bge-m3 \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --knowledge_distillation True \
  --same_dataset_within_batch True \
  --output_dir ./outputs/bge-m3 \
  --overwrite_output_dir \
  --learning_rate 1e-5 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --gradient_checkpointing \
  --negatives_cross_device \
  --sentence_pooling_method cls \
  --normalize_embeddings True \
  --kd_loss_type m3_kd_loss \
  --unified_finetuning True \
  --use_self_distill True
```

## Decoder-Only Embedder

Module:

```bash
python -m FlagEmbedding.finetune.embedder.decoder_only.base --help
```

Use LoRA for large decoder-only models:

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.decoder_only.base \
  --model_name_or_path BAAI/bge-multilingual-gemma2 \
  --use_lora True \
  --lora_rank 32 \
  --lora_alpha 64 \
  --target_modules q_proj k_proj v_proj o_proj gate_proj down_proj up_proj \
  --additional_special_tokens "<instruct>" "<query>" \
  --save_merged_lora_model True \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --query_instruction_for_retrieval "Given a query, retrieve passages that are relevant to the query." \
  --query_instruction_format "<instruct>{}\n<query>{}" \
  --output_dir ./outputs/decoder-embedder \
  --overwrite_output_dir \
  --learning_rate 1e-4 \
  --fp16 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --gradient_checkpointing \
  --sentence_pooling_method last_token
```

Important decoder-only options:

- `--peft_model_path`
- `--use_lora`
- `--lora_rank`, `--lora_alpha`, `--lora_dropout`
- `--target_modules`
- `--use_flash_attn`
- `--use_slow_tokenizer`
- `--additional_special_tokens`
- `--save_merged_lora_model`

## ICL Embedder

Module:

```bash
python -m FlagEmbedding.finetune.embedder.decoder_only.icl --help
```

Use this for `bge-en-icl` style data. Include `type` in JSONL rows when the task requires it, and use ICL-specific prompt formats from the target model card or project docs.

## Encoder-Only Reranker

Module:

```bash
python -m FlagEmbedding.finetune.reranker.encoder_only.base --help
```

Command shape:

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.reranker.encoder_only.base \
  --model_name_or_path BAAI/bge-reranker-v2-m3 \
  --train_data ./train.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --knowledge_distillation False \
  --output_dir ./outputs/reranker-base \
  --overwrite_output_dir \
  --learning_rate 6e-5 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 1 \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --weight_decay 0.01 \
  --logging_steps 10 \
  --save_steps 1000
```

## Decoder-Only Reranker

Base module:

```bash
python -m FlagEmbedding.finetune.reranker.decoder_only.base --help
```

Layerwise module:

```bash
python -m FlagEmbedding.finetune.reranker.decoder_only.layerwise --help
```

Key options:

- `--model_type decoder`
- `--use_lora`, `--lora_rank`, `--lora_alpha`, `--target_modules`
- `--use_flash_attn`
- `--query_instruction_for_rerank`, `--passage_instruction_for_rerank`
- Layerwise: `--start_layer`, `--head_multi`, `--head_type`, `--trust_remote_code`

## Hard-Negative Mining

Use only when the user asks to generate harder negatives. It reads training JSONL and writes a new JSONL file.

```bash
python scripts/mine_hard_negatives.py \
  --input_file train.jsonl \
  --output_file train_minedHN.jsonl \
  --range_for_sampling 2-200 \
  --negative_number 15 \
  --embedder_name_or_path BAAI/bge-base-en-v1.5 \
  --use_gpu_for_searching
```

Important flags:

- `--candidate_pool`: JSONL rows with `text` if using an external pool.
- `--range_for_sampling`: e.g. `2-200`; larger ranges reduce negative difficulty.
- `--negative_number`: number of sampled negatives.
- `--embedder_model_class`: needed for custom embedders.
- `--devices`, `--cache_dir`, `--embedder_batch_size`, max-length flags.

## Teacher Scores

Use teacher scores for distillation.

```bash
python scripts/add_reranker_scores.py \
  --input_file train_minedHN.jsonl \
  --output_file train_score.jsonl \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --reranker_query_max_length 512 \
  --reranker_max_length 1024
```

Important flags:

- `--reranker_model_class`
- `--reranker_peft_path`
- `--use_fp16`, `--use_bf16`
- `--query_instruction_for_rerank`, `--passage_instruction_for_rerank`
- `--normalize`
- `--cutoff_layers`, `--compress_ratio`, `--compress_layers`

## Split By Length

Use this to bucket data by token length before training:

```bash
python scripts/split_by_length.py \
  --input_path train_data \
  --output_dir train_data_split \
  --cache_dir .cache \
  --length_list 0 500 1000 2000 3000 4000 5000 6000 7000 \
  --model_name_or_path BAAI/bge-m3 \
  --num_proc 16
```

Validate inputs before splitting and avoid overwriting outputs unless the user asks for it.
