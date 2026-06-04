---
name: llamafactory-ascend-npu-skill
description: "Use when a user wants LLaMA-Factory Ascend NPU training, FSDP/FSDP2 on NPU, Qwen/Qwen-VL NPU recipes, or NPU QLoRA setup."
disable-model-invocation: true
---

# LLaMA-Factory Ascend NPU

Use this sub-skill when the user asks for Ascend NPU, `ASCEND_RT_VISIBLE_DEVICES`, NPU FSDP/FSDP2, Qwen/Qwen-VL/MoE NPU full tuning, or NPU quantized LoRA.

## Short Workflow

1. Confirm the user is on an Ascend software stack with torch/NPU support before planning a run.
2. Choose the training family: full SFT with FSDP/FSDP2, LoRA SFT, multimodal Qwen-VL SFT, or NPU QLoRA.
3. Generate a public LLaMA-Factory YAML with [scripts/make_ascend_config.py](scripts/make_ascend_config.py), then edit only model, dataset, output, and device-count fields.
4. Pair the training YAML with an Accelerate FSDP/FSDP2 config whose `num_processes` matches visible NPUs.
5. Launch with `accelerate launch --config_file ACCELERATE_CONFIG llamafactory-cli train TRAIN_CONFIG` when using an installed package entry point.
6. Inspect logs for NPU kernel, flash attention, dtype, and process-count failures before scaling the run.

Read [references/configuration.md](references/configuration.md) for recipe choices and field meanings. Read [references/troubleshooting.md](references/troubleshooting.md) for NPU-specific failure modes.

## Scripts

- [scripts/make_ascend_config.py](scripts/make_ascend_config.py): emits minimal NPU training YAML for Qwen, Qwen-MoE, or Qwen-VL style runs.
- [scripts/npu_runtime_env.sh](scripts/npu_runtime_env.sh): optional environment-variable template to read and adapt before launch.

## Boundaries

Use `llamafactory-distributed-train-skill` for generic CUDA torchrun/DeepSpeed/FSDP launch planning. Use `llamafactory-multimodal-sft-skill` for dataset format details when the NPU recipe is vision-language.
