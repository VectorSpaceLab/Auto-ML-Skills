---
name: vllm-and-distributed
description: "Run and debug TRL vLLM generation, trl vllm-serve, Accelerate, DeepSpeed, FSDP, PEFT, quantization, Liger kernels, memory reduction, and multi-GPU training."
---

# vLLM And Distributed

Use this sub-skill when a user asks about speeding up TRL online generation, launching multi-GPU jobs, serving with `trl vllm-serve`, using DeepSpeed/FSDP, or reducing memory use.

## Route By System

- vLLM for GRPO/RLOO generation: read [references/vllm-reference.md](references/vllm-reference.md).
- `trl vllm-serve` command and server-mode generation: read [references/vllm-reference.md](references/vllm-reference.md).
- Accelerate, DeepSpeed, FSDP, PEFT, Liger, and memory reduction: read [references/distributed-and-memory.md](references/distributed-and-memory.md).

## vLLM Install And Smoke Check

```bash
pip install "trl[vllm]"
python -c "import vllm; print(vllm.__version__)"
trl vllm-serve --help
```

Do not treat `import trl` as proof that vLLM works. vLLM depends on compatible Python, CUDA/GPU, PyTorch, and vLLM wheels.

## GRPO/RLOO Colocate Mode

Colocate mode runs vLLM in the trainer process and shares GPU memory with the training model:

```python
from trl import GRPOConfig

args = GRPOConfig(
    output_dir="model-grpo",
    use_vllm=True,
    vllm_mode="colocate",
    vllm_gpu_memory_utilization=0.3,
)
```

Use colocate mode when you want fewer moving parts and can reserve enough GPU memory for both training and generation.

## GRPO/RLOO Server Mode

Start a server:

```bash
trl vllm-serve \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

Point the trainer at the server:

```python
from trl import GRPOConfig

args = GRPOConfig(
    output_dir="model-grpo",
    use_vllm=True,
    vllm_mode="server",
    vllm_server_base_url="http://localhost:8000",
)
```

Use server mode when generation has dedicated GPUs or a separate process is operationally cleaner.

## Distributed Launch

For Python scripts:

```bash
accelerate launch train_sft.py
```

For CLI jobs:

```bash
trl sft --config sft_config.yaml --num_processes 4
```

Use DeepSpeed or FSDP configs only when the user has a concrete memory/scaling need. Keep simple single-GPU or basic multi-GPU launch commands for small models.

## Memory Triage

1. Reduce `per_device_train_batch_size`.
2. Increase `gradient_accumulation_steps`.
3. Lower `max_length` or `max_completion_length`.
4. Enable gradient checkpointing.
5. Use PEFT/LoRA and possibly quantization.
6. For SFT, enable packing when appropriate.
7. Use Liger kernels, FSDP, or DeepSpeed for larger runs.
8. For GRPO/RLOO, use vLLM and tune `num_generations`, `generation_batch_size`, and vLLM memory utilization.

For trainer-specific settings, switch to [../core-trainers/SKILL.md](../core-trainers/SKILL.md).
