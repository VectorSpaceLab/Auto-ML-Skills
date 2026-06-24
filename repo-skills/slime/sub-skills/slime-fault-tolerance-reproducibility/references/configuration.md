# Fault Tolerance And Reproducibility Configuration

## Fault Tolerance

```bash
--use-fault-tolerance
--rollout-health-check-first-wait 600
--rollout-health-check-interval 10
--rollout-health-check-timeout 5
```

Use a larger first wait for models that compile kernels on first generation.

## Resume

```bash
--load /runs/model_slime
--save /runs/model_slime
```

The checkpoint root should contain `latest_checkpointed_iteration.txt`.

## Deterministic Inference And Training

```bash
--sglang-enable-deterministic-inference
--sglang-attention-backend flashinfer
--deterministic-mode
```

Runtime env:

```json
{
  "env_vars": {
    "CUDA_DEVICE_MAX_CONNECTIONS": "1",
    "NCCL_ALGO": "Ring",
    "NVTE_ALLOW_NONDETERMINISTIC_ALGO": "0",
    "CUBLAS_WORKSPACE_CONFIG": ":4096:8"
  }
}
```

Determinism can reduce performance and may depend on kernel/backend support.
