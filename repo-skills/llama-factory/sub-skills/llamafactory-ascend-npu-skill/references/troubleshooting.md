# Ascend NPU Troubleshooting

Read this when an NPU run fails before the first training step or behaves differently from a CUDA recipe.

## Common Failures

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Accelerate starts fewer ranks than expected | `num_processes` does not match visible NPUs | Align Accelerate config with `ASCEND_RT_VISIBLE_DEVICES` |
| Kernel import or unsupported op error | NPU torch/kernel package mismatch | Verify torch/NPU versions and disable optional kernels before retry |
| Flash attention failure | `flash_attn` setting unsupported for that model/kernel | Try `flash_attn: disabled` for LoRA/VLM runs or the documented NPU backend |
| Very slow or timed-out initialization | MoE/VLM model shard setup | Increase `ddp_timeout`, reduce process count, or smoke-test a smaller model |
| OOM during VLM training | Image/video pixel limits too high | Lower `image_max_pixels`, `video_max_pixels`, `cutoff_len`, or batch size |

## Safety Notes

- Do not port CUDA-only quantization or flash-attention flags to NPU without checking backend support.
- Treat NPU QLoRA as backend-specific: validate imports before scheduling a long job.
- If a config uses `use_v1_kernels`, keep a fallback config with the field disabled for debugging.
