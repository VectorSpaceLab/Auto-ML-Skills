---
name: sglang-distributed-topology
description: "Plan and validate SGLang tensor/data/pipeline parallel, multi-node, router, gateway, and prefill-decode disaggregation topologies."
disable-model-invocation: true
---

# SGLang Distributed Topology

Use this sub-skill for TP/DP/PP, multi-node launch plans, router/model gateway, service discovery, Kubernetes, and prefill-decode disaggregation.

Read [references/distributed-topology.md](references/distributed-topology.md). Use [scripts/validate_topology.py](scripts/validate_topology.py) to check topology arithmetic and obvious port/config mistakes before launching.

## Workflow

1. Identify model size, GPU count, nodes, network fabric, and whether the user needs router or direct server.
2. Pick `tp_size`, `dp_size`, `pp_size`, `nnodes`, and `node_rank`; validate that total ranks match available workers.
3. For multi-node, define `--dist-init-addr`, distinct `--node-rank`, and reachable host/ports.
4. For router/model gateway, validate worker URLs and policy before starting traffic.
5. For PD disaggregation, validate prefill/decode endpoints and bootstrap ports before sending generation requests.
