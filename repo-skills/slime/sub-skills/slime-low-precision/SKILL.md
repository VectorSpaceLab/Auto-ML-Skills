---
name: slime-low-precision
description: "Configures slime low-precision workflows including FP8 rollout, FP8 KV cache, FP8 Megatron training, and INT4 rollout or QAT."
disable-model-invocation: true
---

# slime Low Precision

Use this sub-skill when the user asks for FP8, INT4, quantized rollout, FP8 KV cache, or memory-saving low-precision training.

## Short Workflow

1. Decide whether low precision is for rollout only, training only, or both.
2. Stable common path: BF16 Megatron checkpoint for training, FP8 Hugging Face checkpoint for SGLang rollout.
3. Convert HF checkpoint to FP8 or INT4 as needed.
4. Add SGLang low-precision flags such as `--sglang-kv-cache-dtype fp8_e4m3`.
5. For FP8 training, add Megatron/TransformerEngine FP8 flags.

Read [references/workflows.md](references/workflows.md) for FP8/INT4 recipes. Read [references/troubleshooting.md](references/troubleshooting.md) for quantized checkpoint and export pitfalls.

## Scripts

- Adapt [scripts/fp8_rollout_args.sh](scripts/fp8_rollout_args.sh), [scripts/fp8_training_args.sh](scripts/fp8_training_args.sh), or [scripts/int4_rollout_args.sh](scripts/int4_rollout_args.sh).

## Handoff

Use `slime-checkpoint-conversion` for base HF/Megatron conversion and `slime-debug-trace-profile` for validating generation quality before training.
