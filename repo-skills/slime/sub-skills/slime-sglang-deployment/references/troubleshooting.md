# SGLang Deployment Troubleshooting

## CUDA Runtime Symbol Error

If an SGLang worker fails while importing torch with:

```text
libc10_cuda.so: undefined symbol: cudaGetDriverEntryPointByVersion
```

the worker is probably loading an older system `libcudart.so.12` before the CUDA runtime bundled with the installed PyTorch wheel. Use the root `scripts/launch_ray_job_template.sh` launcher or replicate its `LD_LIBRARY_PATH` setup so `torch/lib` and `nvidia/*/lib` from the Python environment come before system CUDA libraries.

## YAML Total GPU Mismatch

Validate:

```bash
python /path/to/skill/slime/scripts/validate_sglang_config.py config.yaml --expected-rollout-gpus 16
```

Then set:

```bash
--rollout-num-gpus 16
--sglang-config config.yaml
```

## External And Managed Modes Mixed

Remove one of:

```bash
--rollout-external
--sglang-config
```

## SGLang OOM

Lower:

```bash
--sglang-mem-fraction-static
```

Under colocate, leave enough memory for Megatron.

## Uneven Multi-Turn Routing

For multi-turn sessions, use:

```bash
--router-policy consistent_hashing
```

This favors session affinity over cache-aware balancing.
