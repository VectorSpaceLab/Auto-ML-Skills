# Distributed And Memory

Read this when scaling TRL training or reducing memory usage.

## Accelerate

Run Python training scripts with:

```bash
accelerate launch train_sft.py
```

TRL CLI can also accept Accelerate-style launch options:

```bash
trl sft --config sft_config.yaml --num_processes 4
```

For multi-node or advanced GPU mapping, create an Accelerate config and keep trainer configuration in YAML or Python separately.

## DeepSpeed And FSDP

Use DeepSpeed/FSDP when model size or optimizer state exceeds basic DDP memory.

DeepSpeed CLI/config style:

```yaml
deepspeed: ds_config.json
```

FSDP style:

```yaml
fsdp: full_shard
fsdp_config:
  activation_checkpointing: true
```

Do not introduce DeepSpeed/FSDP for small single-GPU examples unless the user asks for scaling or memory relief.

## PEFT And Quantization

Install PEFT:

```bash
pip install "trl[peft]"
```

Trainer API:

```python
from peft import LoraConfig
from trl import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen3-0.6B",
    train_dataset=dataset,
    peft_config=LoraConfig(r=32, lora_alpha=16, task_type="CAUSAL_LM"),
)
```

CLI:

```bash
trl sft --config sft_config.yaml --use_peft --lora_r 32 --lora_alpha 16
```

For QLoRA or low-bit training, verify `bitsandbytes` and model-loading kwargs separately.

## Liger Kernels

Install:

```bash
pip install "trl[liger]"
```

Use:

```python
from trl import SFTConfig

args = SFTConfig(use_liger_kernel=True)
```

Liger is useful for peak-memory reduction and throughput on supported model/kernel combinations. If import or kernel errors occur, disable it first to isolate the baseline trainer.

## SFT Packing

Packing is SFT-specific:

```python
from trl import SFTConfig

args = SFTConfig(packing=True, packing_strategy="bfd", max_length=1024)
```

Strategies:

- `"bfd"`: best-fit decreasing; overlong examples are truncated/discard overflow.
- `"bfd_split"`: split overlong examples into chunks before packing.
- `"wrapped"`: concatenate tokens and split into fixed-length blocks.

## OOM Checklist

- Lower `per_device_train_batch_size`.
- Lower `max_length` or `max_completion_length`.
- Use `gradient_accumulation_steps` to restore effective batch size.
- Enable `gradient_checkpointing`.
- Use PEFT/LoRA before full fine-tuning large models.
- Use quantization only after confirming the selected model/backend supports it.
- Use packing for SFT if data has many short examples.
- Use vLLM generation for online methods when generation is the bottleneck.
- Use FSDP or DeepSpeed when model and optimizer states exceed memory.
- For reward training, ensure the sequence-classification head and adapter saved modules are configured correctly.
