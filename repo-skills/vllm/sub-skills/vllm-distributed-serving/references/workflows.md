# Distributed Serving Workflow

## Parallelism Choice

- Tensor parallel: split model weights across GPUs when the model does not fit on one GPU.
- Pipeline parallel: split layers into stages for very large models or topology constraints.
- Data parallel: replicate engines to increase throughput when each replica fits.
- Expert parallel: MoE-specific scaling when model/backend supports it.
- Ray executor: use for multi-node or Ray-managed clusters.
- Multiprocessing executor: common single-node path.

## Multi-Node Discipline

1. Confirm identical vLLM/PyTorch/CUDA or ROCm versions on all nodes.
2. Confirm hostnames, ports, firewall, NCCL interface, and GPU visibility.
3. Start or connect Ray only when needed.
4. Generate commands first; do not launch cluster jobs without explicit user intent.

## Disaggregated Prefill

Disaggregated prefill is an advanced serving mode for separating prefill and decode paths. It is topology- and version-sensitive; start from the public vLLM feature support in the installed package and validate with a small benchmark.
