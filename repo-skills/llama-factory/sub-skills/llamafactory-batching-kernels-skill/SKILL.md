---
name: llamafactory-batching-kernels-skill
description: "Use when a user wants LLaMA-Factory dynamic batching, padding-free training, Liger kernels, Ulysses context parallelism, or batching strategy performance tuning."
disable-model-invocation: true
---

# LLaMA-Factory Batching And Kernels

Use this sub-skill for performance-focused training configs: dynamic batching, padding-free full training, Liger kernels, Ulysses context parallelism, and related throughput tuning.

## Short Workflow

1. Start from a working SFT/full-training config before enabling performance switches.
2. Choose one primary optimization at a time: batching strategy, padding-free mode, Liger kernel, or Ulysses context parallelism.
3. Generate a snippet with [scripts/make_perf_config.py](scripts/make_perf_config.py) and merge it into the user's YAML.
4. Run a short smoke job, compare tokens/sec and loss sanity, then combine optimizations only after each one works alone.

Read [references/configuration.md](references/configuration.md) for switch meanings and compatibility notes. Read [references/troubleshooting.md](references/troubleshooting.md) for common runtime failures.

## Scripts

- [scripts/make_perf_config.py](scripts/make_perf_config.py): emits YAML snippets for `dynamic-batching`, `padding-free`, `liger`, or `ulysses`.

## Boundaries

Use `llamafactory-training-extensions-skill` for optimizer/loss features such as GaLore, APOLLO, BAdam, Muon, FP8, DFT, ASFT, or EAFT.
