---
name: llamafactory-megatron-core-skill
description: "Use when a user wants LLaMA-Factory Megatron-Core full training, tensor/pipeline/expert parallel settings, Qwen-VL MCore, or Qwen MoE MCore recipes."
disable-model-invocation: true
---

# LLaMA-Factory Megatron-Core

Use this sub-skill for full-parameter Megatron-Core style LLaMA-Factory training where configs include tensor, pipeline, sequence, and expert parallel fields.

## Short Workflow

1. Confirm the user needs full-parameter training; the documented MCore recipes are not LoRA-first.
2. Select a model family: Qwen-VL full SFT or Qwen MoE full SFT.
3. Generate a baseline YAML with [scripts/make_mcore_config.py](scripts/make_mcore_config.py).
4. Size tensor, pipeline, and expert parallelism so their product fits the visible GPU count.
5. Launch through the installed LLaMA-Factory CLI and inspect first-step logs before increasing max steps.

Read [references/configuration.md](references/configuration.md) for MCore field meanings and sizing checks. Read [references/troubleshooting.md](references/troubleshooting.md) for parallelism and MoE failures.

## Scripts

- [scripts/make_mcore_config.py](scripts/make_mcore_config.py): emits a Qwen-VL or Qwen MoE full-training YAML skeleton with MCore fields.

## Boundaries

Use `llamafactory-distributed-train-skill` for torchrun/DeepSpeed/Ray launch mechanics. Use `llamafactory-multimodal-sft-skill` for multimodal dataset schemas.
