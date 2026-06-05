---
name: vllm-distributed-serving
description: "Use when a user wants vLLM distributed serving with Ray or multiprocessing, tensor/pipeline/data/expert parallelism, multi-node launch, Kubernetes/Ray Serve patterns, or disaggregated prefill."
disable-model-invocation: true
---

# vLLM Distributed Serving

Use this sub-skill for distributed execution plans and command generation. It owns Ray or multiprocessing backend selection, tensor/pipeline/data/expert parallel plans, multi-node launch mechanics, Kubernetes/Ray Serve patterns, and disaggregated prefill planning.

## Use When

- The user wants to serve a model across multiple GPUs or nodes.
- The user mentions Ray, multiprocessing, tensor parallel, pipeline parallel, data parallel, expert parallel, Ray Serve, Kubernetes, or disaggregated prefill.
- A single-GPU `vllm serve` command works but the user needs more memory or throughput.
- The user needs to debug distributed init, NCCL, Ray worker placement, port reachability, or rank arithmetic.

## Inputs To Collect

- Node count, GPUs per node, GPU type, visible device order, network fabric, container/runtime, and scheduler.
- Model ID, context length, expected memory footprint, desired TP/PP/DP/EP sizes, and whether the model is MoE.
- Backend choice, Ray head address if any, NCCL/env variables, hostnames/IPs, ports, auth, and rollout/rollback plan.

## Short Workflow

1. Gather node count, GPU count, networking, scheduler, model size, target throughput, and whether the model fits on one GPU.
2. Read [references/workflows.md](references/workflows.md) for parallelism selection.
3. Read [references/distributed-reference.md](references/distributed-reference.md) for Ray, multiprocessing, multi-node, data parallel, expert parallel, and disaggregated prefill notes.
4. Run cluster environment checks before launching multi-node work.
5. Generate commands/configs and save them for review; avoid starting multi-node services without explicit user approval.
6. Label node-specific commands clearly and keep health checks for each process.

## Bundled Scripts

- [scripts/make_distributed_command.py](scripts/make_distributed_command.py): builds a `vllm serve` command for TP/PP/DP/Ray settings.
- [scripts/check_cluster_env.py](scripts/check_cluster_env.py): checks Ray/NCCL/env visibility without starting a cluster.

## References

- [references/workflows.md](references/workflows.md): distributed planning workflow.
- [references/distributed-reference.md](references/distributed-reference.md): launch patterns, env variables, and failure modes.

## Boundaries

Use `vllm-serving-config` for single-node arg selection, and `vllm-benchmarks-profiling` to measure throughput after deployment.

## Verification Notes

- Run the cluster checker before launch; it does not start vLLM.
- For a real smoke, verify package import, `vllm serve` health, `/v1/models`, and one short request on the actual topology.
- Do not count a single-GPU Qwen smoke as distributed validation; it only proves the base lifecycle and request path.
