---
name: trl-scaling-integrations
description: Configure TRL for distributed training, memory reduction, speedups, vLLM generation, PEFT/quantization, DeepSpeed/FSDP, Liger, and kernels.
license: Apache-2.0
---

# TRL Scaling And Integrations

Use this sub-skill when a task involves throughput, memory, GPUs, multi-node training, Accelerate, DeepSpeed, FSDP, sequence/context parallelism, vLLM, PEFT, quantization, Liger Kernel, Hub kernels, or optimized attention.

## Decision Path

1. Compute effective batch size with [scripts/effective_batch.py](scripts/effective_batch.py).
2. If memory fails, first reduce `per_device_train_batch_size`, `max_length` / `max_completion_length`, and GRPO/RLOO `num_generations`.
3. For adapter training, use PEFT/LoRA and optionally QLoRA.
4. For long or inefficient SFT data, consider packing, padding-free batching, or chunked loss.
5. For online generation bottlenecks, use vLLM.
6. For multi-GPU or multi-node training, use Accelerate configs, DeepSpeed, FSDP, or context/sequence parallelism based on the bottleneck.
7. For speed, use optimized attention kernels and Liger when compatible.

Read [references/distributed-memory-vllm.md](references/distributed-memory-vllm.md) for operational recipes and [references/integrations-compatibility.md](references/integrations-compatibility.md) for extras and compatibility.

## vLLM Basics

Install:

```bash
pip install "trl[vllm]"
```

Server mode:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 trl vllm-serve --model Qwen/Qwen2.5-7B --tensor-parallel-size 4
CUDA_VISIBLE_DEVICES=4,5,6,7 accelerate launch train.py
```

Set `use_vllm=True, vllm_mode="server"` in `GRPOConfig` or `RLOOConfig`. Keep server and trainer GPUs separate.

Build a server command with [scripts/vllm_server_command.py](scripts/vllm_server_command.py).

## PEFT And Quantization

Install:

```bash
pip install "trl[peft]" "trl[quantization]"
```

CLI:

```bash
trl sft \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/Capybara \
  --use_peft \
  --lora_r 32 \
  --lora_alpha 16 \
  --load_in_4bit
```

Use `lora_task_type=SEQ_CLS` for reward-model adapters.

## Accelerate

For Python scripts:

```bash
accelerate config
accelerate launch train.py
```

For TRL CLI:

```bash
trl sft --model_name_or_path Qwen/Qwen2.5-0.5B --dataset_name trl-lib/Capybara --num_processes 4
```

For DeepSpeed/FSDP, pass an Accelerate config file.

## References

- [references/distributed-memory-vllm.md](references/distributed-memory-vllm.md): Practical recipes for batch size, memory, Accelerate, DeepSpeed/FSDP, context parallelism, and vLLM.
- [references/integrations-compatibility.md](references/integrations-compatibility.md): Optional extras, supported trainer families, and compatibility notes.
- [references/troubleshooting.md](references/troubleshooting.md): OOM, vLLM, distributed, PEFT, quantization, and kernels failures.
