# KTransformers Configuration

Read this when preparing KTransformers-backed LLaMA-Factory training.

## Training YAML Fields

- `use_kt: true`: enables KTransformers integration in the LLaMA-Factory run.
- `kt_weight_path`: optional path to converted expert weights. Use it for INT8/INT4 expert backends; omit it for original BF16 expert weights.
- `finetuning_type: lora`: the documented KT examples use LoRA with `lora_target: all`.
- `trust_remote_code: true`: usually needed by DeepSeek and Qwen MoE model families.

## Accelerate `kt_config` Fields

| Field | Meaning |
| --- | --- |
| `enabled: true` | Turns on KT integration in the accelerate config |
| `kt_backend` | `AMXBF16`, `AMXINT8`, or `AMXINT4` |
| `kt_num_threads` | CPU worker threads for expert execution |
| `kt_tp_enabled` | Enables KT tensor parallelism |
| `kt_threadpool_count` | Number of KT thread pools |
| `kt_max_cache_depth` | Expert execution cache depth |
| `kt_share_backward_bb` | Share backward black-box computation |
| `lora_rank` | Must match the LoRA rank in the training YAML |

## Backend Decision

- Use `AMXBF16` when the expert weights remain in original BF16.
- Use `AMXINT8` or `AMXINT4` only when the expert weights have been converted for that backend.
- Keep `num_processes` aligned with GPU count; KT also consumes CPU capacity, so CPU threads can bottleneck the run.

## Launch Shape

```bash
accelerate launch --config_file kt_accelerate.yaml \
  llamafactory-cli train kt_train.yaml
```

Keep generated configs beside run logs so KT backend and LoRA rank are auditable.
