# RL Training Troubleshooting

## Job Starts But No Resources Are Scheduled

Recalculate GPU needs. Decoupled training requires actor plus rollout GPUs. PPO may also require critic GPUs.

## OOM During Training

Reduce `--max-tokens-per-gpu`, reduce response length, or increase context parallelism. If using dynamic batching, `--micro-batch-size` is ignored.

## SGLang OOM

Lower `--sglang-mem-fraction-static`, especially colocated with training.

## SGLang Worker Torch Import Fails

If a rollout worker fails while importing torch with:

```text
libc10_cuda.so: undefined symbol: cudaGetDriverEntryPointByVersion
```

use the root `scripts/launch_ray_job_template.sh` launcher. It prepends the current Python environment's PyTorch/NVIDIA library directories to `LD_LIBRARY_PATH` and passes that into Ray runtime env, which prevents SGLang child processes from loading an older system CUDA runtime.

## Rewards Are All Same

GRPO benefits from within-group reward variance. Check reward function, labels, and generated response parsing. Consider dynamic sampling filters only after reward correctness is verified.

## Stop Tokens Missing

If generation runs too long, configure stop strings or token IDs:

```bash
--rollout-stop-token-ids <ids>
```
