# vLLM Installation Reference

## Scope

Use this reference after the root `vllm` router when a user asks to install, verify, or choose a vLLM environment. The skill was distilled from vLLM public docs, CLI/API surfaces, examples, and tests, and from read-only inspection of an installed vLLM package. Future agents should use public package installs and this bundled reference, not a private source checkout.

## Environment Baseline

- Python: vLLM supports Python 3.10 through 3.13 in current public docs.
- OS: Linux is the normal production target. macOS Apple Silicon uses the vLLM-Metal ecosystem rather than the standard CUDA wheel path.
- Accelerator: CUDA is the most common path; ROCm, TPU, Ascend, XPU, CPU, and Apple Silicon have platform-specific packages/images or plugins.
- Package check: `python -c "import importlib.metadata as m; print(m.version('vllm'))"`.
- CLI entrypoint: the public console script is `vllm`, with subcommands such as `serve`, `bench`, `chat`, `complete`, `run-batch`, and `collect-env`.

## Install Decision Tree

1. Fresh NVIDIA CUDA environment:

```bash
python -m pip install -U pip uv
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto
python scripts/check_env.py
```

2. Existing environment with compatible PyTorch:

```bash
python -m pip install -U pip
pip install vllm
python scripts/check_env.py --json
```

3. ROCm:

Use public vLLM ROCm wheels or Docker images. `uv pip install vllm --extra-index-url https://wheels.vllm.ai/rocm/` is the public-doc pattern, but ROCm version and glibc compatibility matter.

4. TPU:

Use the public `vllm-tpu` package and TPU-specific docs/images.

5. Ascend:

Use the public vLLM Ascend plugin and its CANN/hardware-matched install instructions.

6. Apple Silicon:

Use vLLM-Metal and MLX-compatible models from public model hubs.

## First Checks

Run these before model loading:

```bash
python scripts/check_env.py --json
python scripts/inspect_api.py --json
vllm --help
vllm serve --help
vllm bench --help
```

Expected signals:

- `vllm` distribution version prints.
- `console_scripts` includes `vllm`.
- Public classes import: `vllm.LLM`, `vllm.SamplingParams`.
- CLI help exits successfully. CLI help may import heavy modules and can be slower than package metadata checks.

## Install Pitfalls

- Do not mix arbitrary PyTorch CUDA wheels with vLLM wheels. Match PyTorch, CUDA/ROCm runtime, and driver.
- If `import vllm` is slow, use `check_env.py` with package metadata first; avoid assuming it is hung until a reasonable timeout has elapsed.
- If GPUs are hidden by `CUDA_VISIBLE_DEVICES`, tensor-parallel sizing and memory checks will be wrong.
- Avoid root-user cache pollution in shared systems; set `HF_HOME`/`TRANSFORMERS_CACHE`/`VLLM_CACHE_ROOT` to a project cache if needed.
- For public skill examples, use public model IDs such as `Qwen/Qwen3-0.6B` or caller-provided IDs. Never rely on local model paths.

## Optional Dependencies

Some workflows need optional packages:

- OpenAI client smoke: `openai` and `requests`.
- YAML validation: `pyyaml`.
- Structured outputs: backend packages may include xgrammar/guidance depending on installed vLLM extras/version.
- Distributed serving: `ray` for Ray executor or Ray Serve paths.
- Bench plotting/dashboard: plotting stack may require additional packages.
- Multimodal: model-specific HF processors and media dependencies may be required.

The bundled scripts degrade gracefully when optional dependencies are missing.
