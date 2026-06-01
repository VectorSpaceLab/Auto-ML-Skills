# Fine-Tuning Troubleshooting

Read this when a FlagEmbedding training command fails or produces unusable outputs.

## Data Validation Fails

Required fields are `query`, `pos`, and `neg`. `pos` and `neg` must be lists of strings. For distillation, score list lengths must match text list lengths.

Fix data before changing trainer flags. Invalid rows often cause late, unclear tokenizer or collator errors.

## No Negatives Available

Training rows need negatives. Use hard-negative mining from the data-preparation sub-skill or sample random negatives from a candidate corpus. Random negatives are acceptable for a first pipeline test but usually weaker for retrieval quality.

## Knowledge Distillation Mismatch

Only set `--knowledge_distillation True` when every row has valid `pos_scores` and `neg_scores`.

Generate scores with the data-preparation reranker-score workflow. Verify that the scoring model is appropriate for the target domain.

## DeepSpeed Config Not Found

Generate configs in the current project:

```bash
python sub-skills/finetuning/scripts/write_deepspeed_config.py --stage 0 --output ds_stage0.json
python sub-skills/finetuning/scripts/write_deepspeed_config.py --stage 1 --output ds_stage1.json
```

Then pass the local path to `--deepspeed`.

## CUDA OOM

Reduce:

```text
--per_device_train_batch_size
--query_max_len
--passage_max_len
--max_len
--train_group_size
```

Enable or keep:

```text
--gradient_checkpointing
--deepspeed ./ds_stage1.json
--fp16 or --bf16, depending on hardware
```

For decoder-only models, use LoRA and keep target modules focused.

## LoRA Target Modules Fail

The examples use:

```text
q_proj k_proj v_proj o_proj
```

for rerankers and:

```text
q_proj k_proj v_proj o_proj gate_proj down_proj up_proj
```

for decoder-only embedders. If the base model uses different module names, inspect the model architecture and adjust `--target_modules`.

## Trust Remote Code

Layerwise MiniCPM examples pass `--trust_remote_code True`. Do not set this for untrusted remote repositories without user approval.

## Slow Or Stalled Training

Check that dataset caching is going to a writable location via `--cache_path`. Use `--max_example_num_per_dataset` for short tests. Increase `--logging_steps` after the pipeline is stable.

## Wrong Pooling Or Instruction Format

Encoder-only BGE examples use `--sentence_pooling_method cls` and `--query_instruction_format "{}{}"`.

Decoder-only examples use `--sentence_pooling_method last_token` and instruction formats like `<instruct>{}\n<query>{}`.

Wrong pooling can produce a model that trains but performs poorly.
