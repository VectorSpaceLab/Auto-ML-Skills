---
name: vllm-distributed-serving
description: "Use when a user wants vLLM distributed serving with Ray or multiprocessing, tensor/pipeline/data/expert parallelism, multi-node launch, Kubernetes/Ray Serve patterns, or disaggregated prefill."
disable-model-invocation: true
---

# vLLM Distributed Serving

Use this sub-skill for distributed execution plans and command generation.

## Short Workflow

1. Gather node count, GPU count, networking, scheduler, model size, target throughput, and whether the model fits on one GPU.
2. Read [references/workflows.md](references/workflows.md) for parallelism selection.
3. Read [references/distributed-reference.md](references/distributed-reference.md) for Ray, multiprocessing, multi-node, data parallel, expert parallel, and disaggregated prefill notes.
4. Run cluster environment checks before launching multi-node work.
5. Generate commands/configs and save them for review; avoid starting multi-node services without explicit user approval.

## Bundled Scripts

- [scripts/make_distributed_command.py](scripts/make_distributed_command.py): builds a `vllm serve` command for TP/PP/DP/Ray settings.
- [scripts/check_cluster_env.py](scripts/check_cluster_env.py): checks Ray/NCCL/env visibility without starting a cluster.

## References

- [references/workflows.md](references/workflows.md): distributed planning workflow.
- [references/distributed-reference.md](references/distributed-reference.md): launch patterns, env variables, and failure modes.

## Boundaries

Use `vllm-serving-config` for single-node arg selection, and `vllm-benchmarks-profiling` to measure throughput after deployment.
