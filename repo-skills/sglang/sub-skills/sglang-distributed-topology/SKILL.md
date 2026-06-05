---
name: sglang-distributed-topology
description: "Plan and validate SGLang tensor/data/pipeline parallel, multi-node, router, gateway, and prefill-decode disaggregation topologies."
disable-model-invocation: true
---

# SGLang Distributed Topology

Use this sub-skill for TP/DP/PP, multi-node launch plans, router/model gateway, service discovery, Kubernetes, expert parallelism, and prefill-decode disaggregation. It is a planning and validation skill first; do not start distributed services until the user has approved hostnames, ports, and resource allocation.

Read [references/distributed-topology.md](references/distributed-topology.md) for launch patterns, router/PD examples, EP/MoE notes, Kubernetes requirements, and failure checks. Use [scripts/validate_topology.py](scripts/validate_topology.py) to check topology arithmetic and obvious port/config mistakes before launching.

## Use When

- The user asks for tensor, data, pipeline, expert, or attention parallel serving.
- The user wants multi-node startup commands, router/model gateway, cache-aware routing, Kubernetes, or PD disaggregation.
- The user needs to scale a working single-node command to multiple GPUs or nodes.
- The user needs to debug distributed init, NCCL, router reachability, or worker health.

## Inputs To Collect

- Nodes, GPUs per node, GPU type, network fabric, container/runtime, visible device order, and firewall rules.
- Model ID, tokenizer, expected memory footprint, desired TP/DP/PP/EP sizes, and whether the model is dense or MoE.
- Hostnames/IPs, HTTP ports, distributed init address, NCCL/bootstrap ports, metrics ports, auth, and service discovery method.

## Workflow

1. Identify model size, GPU count, nodes, network fabric, and whether the user needs router or direct server.
2. Pick `tp_size`, `dp_size`, `pp_size`, `nnodes`, and `node_rank`; validate that total ranks match available workers.
3. For multi-node, define `--dist-init-addr`, distinct `--node-rank`, and reachable host/ports.
4. For router/model gateway, validate worker URLs and policy before starting traffic.
5. For PD disaggregation, validate prefill/decode endpoints and bootstrap ports before sending generation requests.
6. Write commands per node separately and label which process owns each port.

## Verification

- Run the topology validator before launch; it catches arithmetic and common port mistakes without starting SGLang.
- For a real smoke, validate each worker `/health`, then router `/v1/models`, then one short chat/generate request.
- Multi-node, EP, PD, and Kubernetes runs are deployment-specific; record exactly what was actually launched.

## Boundaries

Use `sglang-openai-server` for single-worker lifecycle and client smoke. Use `sglang-cache-performance` for cache/speculative/quantization tuning after topology is healthy. Use `sglang-benchmarks-observability` for throughput comparison after deployment.
