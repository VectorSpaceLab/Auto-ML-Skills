# Megatron-Core Configuration

Read this when adapting LLaMA-Factory configs with Megatron-Core parallelism fields.

## Common Fields

| Field | Use |
| --- | --- |
| `tensor_model_parallel_size` | Splits tensors across GPUs |
| `pipeline_model_parallel_size` | Splits layers across pipeline stages |
| `sequence_parallel` | Often paired with tensor parallelism |
| `use_distributed_optimizer` | Reduces optimizer memory |
| `bias_activation_fusion`, `apply_rope_fusion` | MCore speedups when supported |
| `overlap_param_gather`, `overlap_grad_reduce` | Communication overlap for larger jobs |
| `expert_model_parallel_size` | MoE expert sharding |
| `moe_grouped_gemm`, `moe_token_dispatcher_type` | MoE performance settings |
| `recompute_granularity` | Activation recompute for memory pressure |

## Qwen-VL Pattern

- Use a Qwen-VL template and set `image_max_pixels` / `video_max_pixels`.
- Start with full SFT, moderate `cutoff_len`, and small per-device batch size.
- Tensor plus pipeline parallelism is common for VLM memory pressure.

## Qwen MoE Pattern

- Use full SFT with a Qwen MoE model and template.
- Add expert parallelism and MoE dispatch settings when model size requires it.
- Keep global batch calculation explicit:

```text
global_batch = data_parallel_size * per_device_train_batch_size * gradient_accumulation_steps
data_parallel_size = num_gpus / (tp * pp * ep_if_partitioned)
```

## Scaling Rules

- Parallel sizes must divide the visible GPU count.
- If `sequence_parallel: true`, tensor parallelism should usually be greater than 1.
- Increase `ddp_timeout` for large MoE and VLM initialization.
- Save configs and first-step logs; MCore failures are often configuration-specific.
