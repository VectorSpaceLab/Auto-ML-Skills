# Install, Build, Troubleshooting Reference

## Installation Paths

Common NVIDIA GPU install:

```bash
pip install --upgrade pip
pip install uv
uv pip install sglang
```

Source editable install:

```bash
git clone https://github.com/sgl-project/sglang.git
cd sglang
pip install -e "python"
```

Docker serving pattern:

```bash
docker run --gpus all --shm-size 32g -p 30000:30000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --ipc=host lmsysorg/sglang:latest-runtime \
  python3 -m sglang.launch_server --model-path <MODEL_ID> --host 0.0.0.0 --port 30000
```

Platform docs exist for AMD GPU, CPU server, Apple Metal, Ascend NPU, Intel XPU, TPU, NVIDIA Jetson, and plugin platforms. Choose the platform-specific path when not on a standard NVIDIA/CUDA host.

## Package Extras

Optional extras include:

- `sglang[diffusion]` for diffusion/image/video generation dependencies.
- `sglang[tracing]` for OpenTelemetry tracing.
- `sglang[http2]` for HTTP/2 server support.
- `sglang[checkpoint-engine]`, `sglang[runai]`, `sglang[ray]`, and development/test extras depending on workflow.

## Common Failures

- `CUDA_HOME environment variable is not set`: set it to the CUDA install root or install compatible FlashInfer/kernel wheels first.
- CUDA 13/B300/GB300 ptxas mismatch: use the CUDA 13 runtime image or set `TRITON_PTXAS_PATH` to a toolkit ptxas that supports the GPU.
- Import succeeds but server fails at model load: check driver/toolkit/PyTorch compatibility and model architecture support.
- Grammar import errors: verify `xgrammar`, `llguidance`, `outlines` versions installed by the SGLang release.
- Diffusion CLI missing dependencies: install diffusion extra.
- Router Python module missing: install/build the model gateway/router package for the target environment.

## Environment Variables

High-value env groups:

- Runtime/cache: `SGLANG_CACHE_DIR`, `SGLANG_HOST_IP`, `SGLANG_PORT`, `SGLANG_HEALTH_CHECK_TIMEOUT`.
- Startup/readiness: `SGLANG_WAIT_WEIGHTS_READY_TIMEOUT`.
- Model source: `SGLANG_USE_MODELSCOPE`.
- Performance: `SGLANG_ENABLE_TORCH_COMPILE`, `SGLANG_SET_CPU_AFFINITY`, `SGLANG_IS_FLASHINFER_AVAILABLE`, `SGLANG_SKIP_P2P_CHECK`, `SGLANG_ENABLE_SPEC_V2`.
- Tooling: `SGLANG_TOOL_STRICT_LEVEL`, `SGLANG_FORWARD_UNKNOWN_TOOLS`.
- Profiling/tracing: `SGLANG_TORCH_PROFILER_DIR`, `SGLANG_PROFILE_WITH_STACK`, OpenTelemetry exporter env.
- Kernel debugging: `SGLANG_KERNEL_API_LOGLEVEL`, `SGLANG_KERNEL_API_LOGDEST`, dump include/exclude env.
- Diffusion: `SGLANG_DIFFUSION_TARGET_DEVICE`, `SGLANG_DIFFUSION_ATTENTION_BACKEND`, `SGLANG_DIFFUSION_STAGE_LOGGING`, `SGLANG_DIFFUSION_TORCH_PROFILER_DIR`, Cache-DiT env vars, and cloud-storage env vars.

## Troubleshooting Order

1. Run import/device check.
2. Check `python -m sglang.launch_server --help` or `sglang serve --help`.
3. Validate PyTorch can see the accelerator.
4. Try a tiny public model or placeholder with `--help`/dry-run first, then real launch.
5. Check server logs around model config, tokenizer, attention backend, kernel compilation, and memory planning.
6. Only then reinstall or rebuild kernels.
