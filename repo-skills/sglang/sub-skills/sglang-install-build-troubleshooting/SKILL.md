---
name: sglang-install-build-troubleshooting
description: "Install, build, validate, and troubleshoot SGLang environments, platform backends, custom kernels, and dependency failures."
disable-model-invocation: true
---

# SGLang Install, Build, Troubleshooting

Use this sub-skill for installation, package imports, CUDA/ROCm/CPU/XPU/NPU/TPU platform checks, Docker, source builds, custom kernels, environment variables, and failure diagnosis. Start here when SGLang cannot import, cannot see the accelerator, or fails before an endpoint-specific workflow begins.

Read [references/install-build-troubleshooting.md](references/install-build-troubleshooting.md) for install paths, platform notes, kernel pitfalls, and error triage. Use [scripts/check_install.py](scripts/check_install.py) for lightweight import/package/device checks.

## Use When

- The user asks how to install SGLang or choose pip, Docker, source, CUDA, ROCm, CPU, XPU, NPU, or TPU options.
- `import sglang`, `python -m sglang.launch_server`, custom kernels, FlashInfer, Triton, NCCL, or torch import fails.
- A server fails before `/health` is reachable or exits during model load.
- The user wants a non-destructive diagnosis of a shared machine.

## Inputs To Collect

- OS, Python version, package manager, SGLang version, torch version, accelerator type, driver/runtime versions, and install method.
- The exact command, full traceback, first failing import, GPU visibility, and whether the issue reproduces with a small public model.
- Whether the environment is shared, production, or disposable.

## Workflow

1. Capture platform: OS, Python, GPU/accelerator, driver, CUDA/ROCm/toolkit, Docker or bare metal.
2. Run the check script before proposing reinstall steps.
3. Match install path to platform: pip/uv, Docker runtime image, source editable install, or platform-specific docs.
4. Avoid changing working environments destructively; give reversible commands and note version pinning.
5. Reduce runtime failures to a minimal import or one-prompt server smoke before changing multiple dependencies.

## Verification

- `python scripts/check_install.py --help` is safe; the normal check should avoid loading a model.
- After repair, validate import, CLI discovery, `/health`, and one short request when hardware/model are available.
- Keep local env paths and private package locations out of reusable skill documentation.

## Boundaries

Use `sglang-openai-server` after the package imports and the user needs serving. Use `sglang-offline-runtime` when the package imports but Python-side generation fails. Use `sglang-benchmarks-observability` for performance issues after correctness is established.
