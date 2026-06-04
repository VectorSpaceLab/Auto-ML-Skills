---
name: slime-amd-rocm
description: "Guides agents through slime AMD and ROCm deployment caveats, ROCm Docker choices, AMD launch arguments, and checkpoint conversion adjustments."
disable-model-invocation: true
---

# slime AMD ROCm

Use this sub-skill when the user targets AMD GPUs, ROCm Docker images, MI300/MI325-style hardware, or asks why an NVIDIA-oriented slime command fails on ROCm.

## Short Workflow

1. Prefer a ROCm-specific image or build path; do not reuse CUDA-only Docker instructions.
2. Confirm PyTorch ROCm, SGLang ROCm, and Megatron compatibility.
3. Use AMD-specific launch flags and environment variables.
4. Avoid CUDA-only native kernels and attention backends.
5. Validate with a tiny rollout/training job before scaling.

Read [references/configuration.md](references/configuration.md) for AMD launch differences. Read [references/troubleshooting.md](references/troubleshooting.md) for common ROCm failures.

## Scripts

- Adapt [scripts/amd_runtime_env.sh](scripts/amd_runtime_env.sh).

## Handoff

After hardware/runtime setup, return to the normal RL/SFT/checkpoint skills. The workflow shape is the same; backend flags differ.
