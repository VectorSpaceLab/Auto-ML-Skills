# Distributed Reference

## Parallelism Command Pattern

```bash
vllm serve MODEL \
  --tensor-parallel-size 2 \
  --pipeline-parallel-size 1 \
  --distributed-executor-backend ray
```

Only set Ray backend when Ray is installed and configured. For single-node work, the default backend may be sufficient.

## Parallelism Choices

- Tensor parallel (`--tensor-parallel-size`) splits layers across GPUs and is common when one replica does not fit.
- Pipeline parallel (`--pipeline-parallel-size`) splits layer ranges and can help very large models.
- Data parallel (`--data-parallel-size`) creates replicas for throughput when the model fits per replica.
- Expert parallel is MoE-specific and should be validated with the model's architecture and all-to-all backend.
- Context parallel and disaggregated prefill are advanced deployment modes; generate commands and review topology before launch.

## Dual Batch Overlap

DBO is exposed through parallel/scheduler flags, not a cluster launcher. Use:

```bash
vllm serve MODEL --enable-dbo \
  --dbo-decode-token-threshold 32 \
  --dbo-prefill-token-threshold 512
```

Treat it as a performance experiment. Save baseline and DBO benchmark outputs before changing thresholds.

## Disaggregated Prefill And KV Transfer

Disaggregated prefill/decode uses separate prefill and decode instances and transfers KV cache blocks between them. Current public patterns use `--kv-transfer-config` JSON. NIXL is a common high-performance connector:

```bash
vllm serve MODEL \
  --kv-transfer-config '{"kv_connector":"NixlConnector","kv_role":"kv_producer","kv_load_failure_policy":"fail"}'

vllm serve MODEL \
  --kv-transfer-config '{"kv_connector":"NixlConnector","kv_role":"kv_consumer","kv_load_failure_policy":"fail"}'
```

Important checks:

- Install connector extras such as NIXL in the public runtime environment before launch.
- Align vLLM version, model, block size, attention backend, KV cache dtype, and tensor parallel shape across producer/consumer groups.
- Set side-channel host/port environment variables only for the target deployment and record them in private run logs, not public skill docs.
- For KV cache quantization, producer and consumer cache dtype must match. Runtime dynamic KV scales may not transfer in all connector modes.
- `kv_load_failure_policy="recompute"` can hide transfer problems by recomputing on decode workers; use `"fail"` for smoke validation.

## Kubernetes And Ray Serve

Kubernetes deployment is normally done through public vLLM-compatible stacks such as native manifests, KServe, production-stack, AIBrix, llm-d, or NVIDIA Dynamo. The skill should produce deployment commands/manifests and validation probes, not silently create cluster resources. Check:

- GPU device plugin and container image match the accelerator.
- Model cache or registry access is available on every pod.
- Readiness probes use `/health`; discovery uses `/v1/models`.
- Service routing preserves streaming responses and request timeouts.
- Pod resource limits leave enough shared memory and object-store space for Ray when Ray is used.

Ray Serve LLM can wrap vLLM with autoscaling and routing. Use it when the user explicitly asks for Ray Serve rather than plain `vllm serve`.

## Environment Variables

- `CUDA_VISIBLE_DEVICES`: visible GPU list.
- `NCCL_SOCKET_IFNAME`: network interface for NCCL.
- `NCCL_DEBUG=INFO`: debugging communication failures.
- `RAY_ADDRESS`: connect to an existing Ray cluster when applicable.
- `VLLM_HOST_IP`: pin the node IP used by distributed workers when auto-detection is wrong.
- Connector-specific variables such as NIXL side-channel host/port belong in private deployment configs.

## Failure Modes

- TP size larger than visible GPUs.
- Different package versions across nodes.
- NCCL cannot resolve interface or connect ports.
- Ray object store too small.
- Model cache missing on worker nodes.
- Producer/consumer KV transfer config mismatch.
- Kubernetes service or ingress buffering streamed responses.
- Ray Serve autoscaling cold starts confused with vLLM model-load failures.
