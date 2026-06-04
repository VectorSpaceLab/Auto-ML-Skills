# slime Troubleshooting

Read this when a slime workflow fails before launch, during Ray scheduling, during rollout generation, or during Megatron training.

## Import And Parser Failures

Symptom:

```text
ModuleNotFoundError: No module named 'megatron.training'
```

Cause: the environment has `megatron-core` but not the full Megatron-LM checkout on `PYTHONPATH`.

Fix:

```bash
export PYTHONPATH=/path/to/Megatron-LM:${PYTHONPATH}
python /path/to/skill/slime/scripts/check_env.py --strict-train
```

Symptom:

```text
deep_ep is not installed, some functionalities may be limited.
```

Cause: optional DeepEP backend is missing. It may be acceptable for non-DeepEP topologies. For MoE/EP jobs that require DeepEP, use the official Docker image or install the matching backend.

## Ray Job Stuck On Submission

Check whether training and rollout resources fit the cluster.

For colocated jobs, total GPUs must be at least:

```text
actor_num_nodes * actor_num_gpus_per_node
```

For decoupled jobs, total GPUs must be at least:

```text
actor_num_nodes * actor_num_gpus_per_node + rollout_num_gpus
```

Also confirm that `--colocate` is set when training and inference share the same GPUs.

Symptom:

```text
AF_UNIX path length cannot exceed 107 bytes
.../ray/session_.../sockets/plasma_store
```

Cause: Ray's temp directory is nested so deeply that its Unix socket path exceeds the OS limit.

Fix:

```bash
export RAY_TMPDIR=/tmp/ray
mkdir -p "${RAY_TMPDIR}"
```

Set this before `ray start` or before using the bundled launch template.

## Garbled Text Or Bad Generation

The usual cause is a Megatron checkpoint load mismatch. Megatron loads a checkpoint directory, not a single iteration subdirectory. A valid `torch_dist` checkpoint root normally contains:

```text
latest_checkpointed_iteration.txt
release/ or iter_0000001/
  *.distcp
```

Use `--ckpt-step` to select a specific iteration when needed. For actor resume, set `--load` to the same root used by `--save`; if `--load` is absent or invalid, slime initializes from `--ref-load`.

## SGLang Startup Or Health Failures

Port conflicts can surface as `/get_model_info` or connection retry errors. Stop old Ray/SGLang processes before reruns:

```bash
ray stop --force || true
pkill -f sglang || true
```

For large MoE models, first startup may compile kernels. Increase:

```bash
--rollout-health-check-first-wait 600
--rollout-health-check-timeout 30
```

SGLang illegal memory access can be OOM. Lower:

```bash
--sglang-mem-fraction-static 0.5
```

Symptom:

```text
ImportError: .../torch/lib/libc10_cuda.so: undefined symbol: cudaGetDriverEntryPointByVersion, version libcudart.so.12
```

Cause: an SGLang multiprocessing child process is loading an older system `libcudart.so.12` instead of the CUDA runtime bundled with the installed PyTorch wheel. This can happen when `LD_LIBRARY_PATH` points at a system CUDA toolkit before the Python package libraries.

Fix: start Ray jobs through [../scripts/launch_ray_job_template.sh](../scripts/launch_ray_job_template.sh), which prepends the current Python environment's `torch/lib` and `nvidia/*/lib` directories to `LD_LIBRARY_PATH` before `ray start` and in Ray runtime env JSON. If writing a custom launcher, apply the same rule before launching SGLang.

For long generation with no stop, verify stop tokens or set:

```bash
--rollout-stop-token-ids <id1> <id2>
```

## Training OOM

If using dynamic batching, reduce:

```bash
--max-tokens-per-gpu
```

Start with roughly:

```text
rollout_max_response_len / context_parallel_size
```

If custom multi-turn generation makes samples much longer than expected, save rollout dumps and inspect lengths before increasing training memory.

## Bad Or Unstable Gradients

Check data template compatibility first. If the dataset already includes a chat template, do not apply a mismatched tokenizer template again. For NaN/Inf guardrail experiments, slime exposes:

```bash
--no-check-for-nan-in-loss-and-grad
```

Use this as a debugging bypass, not as proof that the data/model setup is healthy.

## Debug Isolation

Separate rollout and training problems:

```bash
--debug-rollout-only
--save-debug-rollout-data /path/to/rollout_{rollout_id}.pt
```

Then replay training side:

```bash
--debug-train-only
--load-debug-rollout-data /path/to/rollout_{rollout_id}.pt
```

For memory measurement while keeping engines live, use the forge replay path documented in the debug sub-skill.
