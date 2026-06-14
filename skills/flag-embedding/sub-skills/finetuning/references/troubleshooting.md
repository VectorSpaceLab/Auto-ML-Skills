# Fine-Tuning Troubleshooting

Read this when a FlagEmbedding training or data-preparation workflow fails.

## Validate Data First

Run:

```bash
python scripts/validate_finetune_jsonl.py train.jsonl --task embedder
```

For distillation:

```bash
python scripts/validate_finetune_jsonl.py train.jsonl --require-scores
```

Fix all schema errors before launching `torchrun`.

## Missing Train Data

The data argument classes check that each `--train_data` path exists and raise `FileNotFoundError` if not. Use absolute or working-directory-correct paths in generated commands.

If the user passes a directory, confirm it contains JSONL files matching the required row schema.

## Knowledge Distillation Errors

If `--knowledge_distillation True` is set:

- Include `pos_scores` and `neg_scores`.
- Align each scores list to the corresponding `pos` or `neg` list.
- Use numeric scores.
- Confirm `--kd_loss_type` matches the model family; M3 examples use `m3_kd_loss`.

## CUDA, Deepspeed, And Flash Attention

`FlagEmbedding[finetune]` may involve CUDA-sensitive packages. If installation or import fails:

- Verify `python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"`.
- Confirm the torch wheel matches the host GPU driver.
- Install `flash-attn` only for workflows that actually use `--use_flash_attn`.
- Use `--deepspeed` only after deepspeed imports and the config is valid.
- Avoid Python versions without wheels for torch, deepspeed, or flash-attn.

## Out Of Memory

Reduce memory pressure:

- Lower `--per_device_train_batch_size`.
- Increase `--gradient_accumulation_steps`.
- Reduce `--train_group_size`.
- Shorten `--query_max_len`, `--passage_max_len`, or `--max_len`.
- Disable `--negatives_cross_device`.
- Use gradient checkpointing when supported.
- Use LoRA for decoder-only models.
- Move from a large to base/small model for smoke tests.

## Wrong Module

Choose the module by model family:

- BGE v1/v1.5 encoder embedder: `embedder.encoder_only.base`.
- BGE-M3: `embedder.encoder_only.m3`.
- Decoder-only embedder: `embedder.decoder_only.base`.
- ICL embedder: `embedder.decoder_only.icl`.
- Encoder-only reranker: `reranker.encoder_only.base`.
- Decoder-only reranker: `reranker.decoder_only.base`.
- Layerwise reranker: `reranker.decoder_only.layerwise`.

If the model requires remote code, pass `--trust_remote_code True` only after the user accepts the risk.

## Checkpoint Output Problems

If no checkpoint appears:

- Check `--output_dir`.
- Check `--save_steps` relative to total steps.
- Check whether training exited before the first save.
- Use `--overwrite_output_dir` only when the user wants existing contents overwritten.

For LoRA workflows, decide whether to save adapters only or use `--save_merged_lora_model True`.
