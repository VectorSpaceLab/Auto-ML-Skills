---
name: llamafactory-ktransformers-skill
description: "Use when a user wants LLaMA-Factory KTransformers training, MoE LoRA with use_kt, FSDP2 kt_config, AMX BF16/INT8/INT4 backends, or kt_weight_path setup."
disable-model-invocation: true
---

# LLaMA-Factory KTransformers

Use this sub-skill for KTransformers-backed MoE fine-tuning, especially DeepSeek and Qwen MoE LoRA runs that combine LLaMA-Factory YAML with an Accelerate FSDP2 `kt_config`.

## Short Workflow

1. Confirm KTransformers is installed and that the target model is an MoE model supported by the chosen KT backend.
2. Choose expert backend: `AMXBF16` for original BF16 experts, `AMXINT8` or `AMXINT4` for converted expert weights.
3. Generate a training YAML with [scripts/make_kt_train_config.py](scripts/make_kt_train_config.py).
4. Generate or adapt an Accelerate FSDP2 config with [scripts/make_kt_accelerate_config.py](scripts/make_kt_accelerate_config.py).
5. If using INT8/INT4 experts, set `kt_weight_path` to the converted expert-weight directory.
6. Launch with `accelerate launch --config_file KT_ACCELERATE.yaml llamafactory-cli train KT_TRAIN.yaml`.

Read [references/configuration.md](references/configuration.md) for backend choices and config fields. Read [references/troubleshooting.md](references/troubleshooting.md) for KT import, memory, and weight-path failures.

## Scripts

- [scripts/make_kt_train_config.py](scripts/make_kt_train_config.py): emits a minimal MoE LoRA training config with `use_kt: true`.
- [scripts/make_kt_accelerate_config.py](scripts/make_kt_accelerate_config.py): emits an FSDP2 Accelerate config with `kt_config`.

## Boundaries

Use `llamafactory-distributed-train-skill` for generic FSDP2 launch mechanics. Use `llamafactory-adapter-variants-skill` when the user asks about LoRA variants unrelated to KT.
