# Ascend NPU Configuration

Read this when preparing LLaMA-Factory jobs for Ascend NPUs.

## Recipe Selection

| User goal | Start with |
| --- | --- |
| Full-parameter Qwen SFT on NPU | `stage: sft`, `finetuning_type: full`, FSDP/FSDP2 accelerate config |
| Qwen MoE full tuning | full SFT plus long `ddp_timeout`, `save_only_model: true`, and MoE-compatible template |
| Qwen-VL or Qwen-VL-MoE SFT | multimodal model fields plus `image_max_pixels`, `video_max_pixels`, Qwen-VL template |
| NPU LoRA | `finetuning_type: lora`, `lora_target: all`, NPU-visible devices |
| NPU QLoRA | quantized LoRA recipe; confirm quantization backend is supported by the installed NPU stack |

## Common YAML Fields

- `use_v1_kernels: true`: enables newer LLaMA-Factory kernels used by the project NPU examples.
- `flash_attn: fa2` or `flash_attn: disabled`: select according to model and NPU kernel support. Some VLM LoRA recipes disable flash attention.
- `bf16: true`: preferred dtype in the documented NPU examples.
- `ddp_timeout`: large values are common for MoE/VLM runs because initialization can be slow.
- `ASCEND_RT_VISIBLE_DEVICES`: NPU equivalent of CUDA device selection. Keep it outside public config files.
- Accelerate `num_processes`: must match the number of visible NPU processes for the selected FSDP/FSDP2 config.

## Launch Shape

Use an installed LLaMA-Factory CLI and generated configs:

```bash
ASCEND_RT_VISIBLE_DEVICES=0,1,2,3 \
accelerate launch --config_file accelerate_fsdp2.yaml \
  llamafactory-cli train ascend_train.yaml
```

For public-ready skills, bundle or generate the YAML to be launched; do not depend on an original example path being present.

## Scaling Checks

- Global batch is `num_processes * per_device_train_batch_size * gradient_accumulation_steps`.
- Match `cutoff_len`, media pixel limits, and batch size to NPU memory.
- Confirm model template: Qwen base/chat, Qwen3 thinking/no-thinking, and Qwen-VL templates are not interchangeable.
- For VLM runs, validate dataset media paths before launch.
