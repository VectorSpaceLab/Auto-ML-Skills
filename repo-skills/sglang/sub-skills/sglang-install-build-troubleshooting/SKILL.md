---
name: sglang-install-build-troubleshooting
description: "Install, build, validate, and troubleshoot SGLang environments, platform backends, custom kernels, and dependency failures."
disable-model-invocation: true
---

# SGLang Install, Build, Troubleshooting

Use this sub-skill for installation, package imports, CUDA/ROCm/CPU/XPU/NPU/TPU platform checks, Docker, source builds, custom kernels, environment variables, and failure diagnosis.

Read [references/install-build-troubleshooting.md](references/install-build-troubleshooting.md). Use [scripts/check_install.py](scripts/check_install.py) for lightweight import/package/device checks.

## Workflow

1. Capture platform: OS, Python, GPU/accelerator, driver, CUDA/ROCm/toolkit, Docker or bare metal.
2. Run the check script before proposing reinstall steps.
3. Match install path to platform: pip/uv, Docker runtime image, source editable install, or platform-specific docs.
4. Avoid changing working environments destructively; give reversible commands and note version pinning.
