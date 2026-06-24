# slime Installation And Runtime Requirements

Read this when preparing a slime environment, choosing Docker vs source install, or diagnosing whether an installed package can run training.

## What Must Be Present

slime is a distributed post-training framework, not a standalone lightweight trainer. A usable training environment normally needs:

- Python `>=3.10`.
- The `slime` package importable as `import slime`.
- `slime_plugins` importable for model bridge and plugin code.
- Ray with dashboard/job support.
- SGLang and `sglang-router`.
- A full Megatron-LM checkout on `PYTHONPATH`, not only the `megatron-core` package. The training parser imports `megatron.training.arguments`.
- CUDA-compatible native dependencies for the selected hardware, attention backend, and optional low-precision path.
- Hugging Face checkpoints for SGLang/tokenizer initialization.
- Megatron-format checkpoints, usually `torch_dist`, for training/ref/critic loads.

The public Docker image is the stable path because slime tracks patched versions of SGLang, Megatron-LM, and native kernels.

## Docker Path

Use Docker when the user wants the quickest path to a known-compatible stack:

```bash
docker pull slimerl/slime:latest
docker run --rm --gpus all --ipc=host --shm-size=16g \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -it slimerl/slime:latest /bin/bash
```

Inside the container, updating slime source follows the public repo pattern:

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -e . --no-deps
```

Do not let `pip` re-resolve CUDA-heavy dependencies unless you intend to rebuild the stack; `--no-deps` protects the pinned image.

## Source Install Path

Use source install only when the user needs custom patches or cannot use Docker. The public `build_conda.sh` documents the expected component families: SGLang, Megatron-LM, patched router, TransformerEngine, Apex, modelopt, flash attention, and other native kernels.

Minimal package install commands:

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -r requirements.txt
pip install -e . --no-deps
```

This makes `import slime` work, but it is not enough for Megatron-backed training unless the full Megatron-LM tree is also available:

```bash
export PYTHONPATH=/path/to/Megatron-LM:${PYTHONPATH}
python /path/to/skill/slime/scripts/check_env.py --strict-train
```

## Runtime Entrypoints

slime does not expose a verified `slime` CLI. Public workflows normally run a source script with Ray:

```bash
ray start --head --node-ip-address 127.0.0.1 --num-gpus 8 --disable-usage-stats
ray job submit --address="http://127.0.0.1:8265" \
  --runtime-env-json='{"env_vars":{"PYTHONPATH":"/path/to/Megatron-LM","CUDA_DEVICE_MAX_CONNECTIONS":"1"}}' \
  -- python /path/to/skill/slime/scripts/run_slime_train.py ...
```

Use `scripts/run_slime_train.py` for synchronous rollout/train/update loops and `scripts/run_slime_train_async.py` for async training flows. These bundled runners avoid requiring the original slime checkout's `train.py`.

## Minimum Verification

Run:

```bash
python /path/to/skill/slime/scripts/check_env.py
```

Expected result:

- `slime` import succeeds.
- `slime_plugins` import succeeds.
- Core dataclasses and rollout modules import.
- Package version is reported.

Then run strict training verification:

```bash
python /path/to/skill/slime/scripts/check_env.py --strict-train --megatron-path /path/to/Megatron-LM
```

Expected result:

- `megatron.training.arguments` import succeeds.
- slime Megatron backend argument module import succeeds.

If strict mode fails, do not start a Ray job yet. Fix `PYTHONPATH`, Megatron checkout version, or the Docker/source installation first.
