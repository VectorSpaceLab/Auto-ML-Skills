# Training Workflows

Read this for FlagEmbedding fine-tuning command templates. These commands are adapted from the repository examples and avoid source-repo-relative paths.

## General Pattern

1. Install `FlagEmbedding[finetune]`.
2. Validate training JSONL.
3. Generate DeepSpeed config if using `--deepspeed`.
4. Start with one node and small batch sizes.
5. Scale `--nproc_per_node`, batch size, sequence length, and epochs after a short successful run.

Set:

```bash
export WANDB_MODE=disabled
```

when you do not want Weights & Biases logging.

## Encoder-Only Embedder

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.encoder_only.base \
  --model_name_or_path BAAI/bge-large-en-v1.5 \
  --cache_dir ./cache/model \
  --train_data ./train/retrieval.jsonl ./train/sts.jsonl \
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
  --deepspeed ./ds_stage0.json \
  --logging_steps 10 \
  --save_steps 1000 \
  --negatives_cross_device \
  --temperature 0.02 \
  --sentence_pooling_method cls \
  --normalize_embeddings True \
  --kd_loss_type kl_div
```

## BGE-M3 Embedder

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.encoder_only.m3 \
  --model_name_or_path BAAI/bge-m3 \
  --cache_dir ./cache/model \
  --train_data ./train/retrieval.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --knowledge_distillation True \
  --same_dataset_within_batch True \
  --small_threshold 0 \
  --drop_threshold 0 \
  --output_dir ./outputs/bge-m3-ft \
  --overwrite_output_dir \
  --learning_rate 1e-5 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --deepspeed ./ds_stage0.json \
  --logging_steps 10 \
  --save_steps 1000 \
  --negatives_cross_device \
  --temperature 0.02 \
  --sentence_pooling_method cls \
  --normalize_embeddings True \
  --kd_loss_type m3_kd_loss \
  --unified_finetuning True \
  --use_self_distill True \
  --fix_encoder False \
  --self_distill_start_step 0
```

## Decoder-Only Embedder

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.decoder_only.base \
  --model_name_or_path BAAI/bge-multilingual-gemma2 \
  --cache_dir ./cache/model \
  --use_lora True \
  --lora_rank 32 \
  --lora_alpha 64 \
  --target_modules q_proj k_proj v_proj o_proj gate_proj down_proj up_proj \
  --additional_special_tokens "<instruct>" "<query>" \
  --save_merged_lora_model True \
  --train_data ./train/retrieval.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --query_instruction_for_retrieval "Given a query, retrieve passages that are relevant to the query." \
  --query_instruction_format "<instruct>{}\n<query>{}" \
  --knowledge_distillation False \
  --output_dir ./outputs/llm-embedder-ft \
  --overwrite_output_dir \
  --learning_rate 1e-4 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --deepspeed ./ds_stage1.json \
  --logging_steps 10 \
  --save_steps 1000 \
  --negatives_cross_device \
  --temperature 0.02 \
  --sentence_pooling_method last_token \
  --normalize_embeddings True \
  --kd_loss_type m3_kd_loss
```

## ICL Decoder-Only Embedder

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.embedder.decoder_only.icl \
  --model_name_or_path BAAI/bge-en-icl \
  --cache_dir ./cache/model \
  --use_lora True \
  --lora_rank 32 \
  --lora_alpha 64 \
  --target_modules q_proj k_proj v_proj o_proj gate_proj down_proj up_proj \
  --additional_special_tokens "<instruct>" "<query>" "<response>" \
  --save_merged_lora_model True \
  --train_data ./train/retrieval.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 2048 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --query_instruction_for_retrieval "Given a query, retrieve passages that are relevant to the query." \
  --query_instruction_format "<instruct>{}\n<query>{}" \
  --knowledge_distillation True \
  --same_dataset_within_batch True \
  --small_threshold 0 \
  --drop_threshold 0 \
  --example_query_max_len 256 \
  --example_passage_max_len 256 \
  --retrieval_use_examples True \
  --icl_suffix_str "\n<response>" \
  --output_dir ./outputs/bge-en-icl-ft \
  --overwrite_output_dir \
  --learning_rate 1e-4 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --deepspeed ./ds_stage1.json \
  --logging_steps 10 \
  --save_steps 1000 \
  --negatives_cross_device \
  --temperature 0.02 \
  --sentence_pooling_method last_token \
  --normalize_embeddings True \
  --kd_loss_type kl_div
```

## Encoder-Only Reranker

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.reranker.encoder_only.base \
  --model_name_or_path BAAI/bge-reranker-base \
  --cache_dir ./cache/model \
  --train_data ./train/reranker.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 256 \
  --passage_max_len 256 \
  --pad_to_multiple_of 8 \
  --knowledge_distillation True \
  --output_dir ./outputs/reranker-base-ft \
  --overwrite_output_dir \
  --learning_rate 6e-5 \
  --fp16 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 1 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --weight_decay 0.01 \
  --deepspeed ./ds_stage0.json \
  --logging_steps 10 \
  --save_steps 1000
```

## Decoder-Only Reranker

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.reranker.decoder_only.base \
  --model_name_or_path BAAI/bge-reranker-v2-gemma \
  --cache_dir ./cache/model \
  --use_lora True \
  --lora_rank 32 \
  --lora_alpha 64 \
  --use_flash_attn True \
  --target_modules q_proj k_proj v_proj o_proj \
  --save_merged_lora_model True \
  --model_type decoder \
  --train_data ./train/reranker_prompt.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --knowledge_distillation True \
  --query_instruction_for_rerank "A: " \
  --query_instruction_format "{}{}" \
  --passage_instruction_for_rerank "B: " \
  --passage_instruction_format "{}{}" \
  --output_dir ./outputs/llm-reranker-ft \
  --overwrite_output_dir \
  --learning_rate 2e-4 \
  --bf16 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 1 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --weight_decay 0.01 \
  --deepspeed ./ds_stage0.json \
  --logging_steps 10 \
  --save_steps 1000
```

## Layerwise Reranker

```bash
torchrun --nproc_per_node 2 \
  -m FlagEmbedding.finetune.reranker.decoder_only.layerwise \
  --model_name_or_path BAAI/bge-reranker-v2-minicpm-layerwise \
  --cache_dir ./cache/model \
  --use_lora True \
  --lora_rank 32 \
  --lora_alpha 64 \
  --use_flash_attn True \
  --target_modules q_proj k_proj v_proj o_proj \
  --save_merged_lora_model True \
  --model_type decoder \
  --start_layer 8 \
  --head_multi True \
  --head_type simple \
  --trust_remote_code True \
  --train_data ./train/reranker_prompt.jsonl \
  --cache_path ./cache/data \
  --train_group_size 8 \
  --query_max_len 512 \
  --passage_max_len 512 \
  --pad_to_multiple_of 8 \
  --knowledge_distillation True \
  --query_instruction_for_rerank "A: " \
  --query_instruction_format "{}{}" \
  --passage_instruction_for_rerank "B: " \
  --passage_instruction_format "{}{}" \
  --output_dir ./outputs/layerwise-reranker-ft \
  --overwrite_output_dir \
  --learning_rate 2e-4 \
  --bf16 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 1 \
  --dataloader_drop_last True \
  --warmup_ratio 0.1 \
  --gradient_checkpointing \
  --weight_decay 0.01 \
  --deepspeed ./ds_stage0.json \
  --logging_steps 10 \
  --save_steps 1000
```

## Scaling Notes

Use `--negatives_cross_device` for embedder training when multiple devices should contribute in-batch negatives.

Use `--same_dataset_within_batch True` when mixing heterogeneous datasets and wanting batches to remain internally consistent.

For decoder-only LLM training, LoRA plus `--gradient_checkpointing` and DeepSpeed stage 1 are common starting points.

For BF16-capable hardware, prefer `--bf16` for large decoder-only rerankers when the model and hardware support it.
