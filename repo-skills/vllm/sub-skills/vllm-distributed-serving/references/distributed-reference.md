# Distributed Reference

## Command Pattern

```bash
vllm serve MODEL \
  --tensor-parallel-size 2 \
  --pipeline-parallel-size 1 \
  --distributed-executor-backend ray
```

Only set Ray backend when Ray is installed and configured. For single-node work, the default backend may be sufficient.

## Environment Variables

- `CUDA_VISIBLE_DEVICES`: visible GPU list.
- `NCCL_SOCKET_IFNAME`: network interface for NCCL.
- `NCCL_DEBUG=INFO`: debugging communication failures.
- `RAY_ADDRESS`: connect to an existing Ray cluster when applicable.

## Failure Modes

- TP size larger than visible GPUs.
- Different package versions across nodes.
- NCCL cannot resolve interface or connect ports.
- Ray object store too small.
- Model cache missing on worker nodes.
