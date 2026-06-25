# Fine-tuning Troubleshooting

## Optional dependency failures

Symptom: import or launch errors for `deepspeed`, `flash_attn`, `datasets`, `peft`, or training-only integrations.

Actions:

- Install fine-tune extras with `pip install 'FlagEmbedding[finetune]'` in the active environment.
- Only install DeepSpeed when using `--deepspeed`; verify it matches the CUDA/PyTorch stack.
- Only enable `--use_flash_attn True` when flash-attn is installed and compatible; otherwise omit it.
- If `--bf16` fails, switch to `--fp16` or full precision depending on hardware support.
- If a model requires custom code, use `--trust_remote_code True` only after the user approves remote code execution risk.

## JSONL schema failures

Symptoms: dataset load errors, `KeyError`, empty batches, or distillation loss shape errors.

Actions:

- Run `python scripts/validate_finetune_jsonl.py --input train.jsonl --mode embedder --require-negatives`.
- Add `--check-scores` when `--knowledge_distillation True`.
- Ensure `query` is a non-empty string, `pos` is a non-empty list, and `neg` is a list with enough non-empty strings.
- Ensure `pos_scores` length equals `pos` length and `neg_scores` length equals `neg` length.
- Convert string scores like `"0.92"` into numeric JSON values like `0.92`.
- For ICL embedder data, keep `type` values consistent and provide `prompt`/instruction fields deliberately.

## `train_data` path problems

Symptoms: no examples loaded, wrong datasets mixed, or path parsing issues.

Actions:

- Pass one or more explicit JSONL files or directories after `--train_data`.
- Quote paths with spaces.
- Validate every JSONL in a directory before training.
- When using `same_dataset_within_batch=True`, verify each directory/file is large enough for batch construction.
- For tiny smoke tests, set `small_threshold=0` and `drop_threshold=0` so small datasets are not dropped.

## Batch and group-size issues

Symptoms: sampling errors, repeated negatives, very small effective batches, or contrastive loss instability.

Actions:

- Keep `train_group_size <= 1 + min(len(neg))` unless using loader behavior that samples from larger datasets.
- Mine or sample more negatives before increasing `train_group_size`.
- Use `same_dataset_within_batch=True` only when within-dataset negatives are desired and dataset sizes support it.
- If `dataloader_drop_last=True`, tiny datasets may produce no steps; lower batch size or disable drop-last for smoke tests.

## GPU memory failures

Symptoms: CUDA OOM during forward/backward, especially with decoder-only, ICL, or long reranker pairs.

Actions:

- Lower `per_device_train_batch_size` first.
- Increase `gradient_accumulation_steps` to preserve effective batch size.
- Enable `--gradient_checkpointing` if not already enabled.
- Use `--sub_batch_size` for embedder training when available.
- Lower `query_max_len`, `passage_max_len`, `max_len`, `example_query_max_len`, or `example_passage_max_len`.
- Split data by length and train long buckets with smaller batch settings.
- Disable `--negatives_cross_device` if communication or memory overhead is too high.
- For decoder models, use LoRA and avoid full fine-tuning unless resources are sufficient.

## DeepSpeed issues

Symptoms: config file not found, launcher errors, ZeRO configuration mismatch, or output checkpoint surprises.

Actions:

- Ensure the `--deepspeed` path points to a real JSON config in the current project.
- Use stage 0 as a conservative baseline; use stage 1 for larger decoder jobs when appropriate.
- Keep `torchrun --nproc_per_node` aligned with visible GPUs.
- Confirm `CUDA_VISIBLE_DEVICES` before launch.
- If debugging, remove DeepSpeed and run a one-process tiny smoke test first.

## Output directory and cache issues

Symptoms: accidental overwrite, permission errors, stale tokenized data, or checkpoint download failures.

Actions:

- Review `--output_dir` before using `--overwrite_output_dir`.
- Use separate `cache_path` values after changing tokenization, instructions, sequence lengths, or dataset content.
- Use writable model/data cache directories.
- For private or gated models, configure tokens through the environment or approved credential flow; do not write secrets into skill files.

## Hard-negative mining issues

Symptoms: FAISS import errors, too few negatives, positives appearing as negatives, or mining too easy/hard.

Actions:

- Use CPU FAISS unless GPU FAISS is installed and approved.
- Validate candidate pool lines have `text`.
- Ensure candidate pool size is much larger than `negative_number`.
- Increase `range_for_sampling` right bound if too few candidates survive filtering.
- Increase the left bound, for example from `2-200` to `60-300`, when negatives are too hard or false-negative-prone.
- Align mining model instructions with the target training family.
- Treat mining as an inference job that may download checkpoints.

## Teacher-score issues

Symptoms: score length mismatch, OOM in teacher scoring, or poor distillation signal.

Actions:

- Validate scored output with `--check-scores`.
- Reduce `reranker_batch_size` when scoring OOMs.
- Keep prompt/instruction formatting consistent between teacher scoring and training.
- Use a teacher checkpoint appropriate for the language/domain.
- If using M3 distillation, prefer `kd_loss_type=m3_kd_loss` for M3 command families.

## Choosing the wrong family

Use encoder-only embedder when training conventional BGE embedding models. Use M3 for `BAAI/bge-m3` and multi-vector/sparse unified behavior. Use decoder-only embedder for generative decoder checkpoints with LoRA and `last_token` pooling. Use ICL only when data has ICL task metadata and examples. Use encoder reranker for BERT-style pair scoring. Use decoder reranker for LLM-style pair scoring. Use layerwise reranker only when the checkpoint and serving plan need layerwise outputs.
