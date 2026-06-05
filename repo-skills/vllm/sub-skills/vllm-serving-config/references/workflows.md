# Serving Configuration Workflow

## Steps

1. Decide mode: offline API, `vllm serve`, benchmark, or distributed.
2. Choose model and runner.
3. Map hardware to parallelism:
   - one GPU: no TP/PP
   - model split across GPUs: tensor parallel
   - very large model or pipeline needs: pipeline parallel
   - replicas for throughput: data parallel or external load balancer
4. Choose memory controls: `max-model-len`, `gpu-memory-utilization`, CPU offload/swap only if needed.
5. Add optional features: quantization, LoRA, prefix caching, speculative decoding, custom chat template.
6. Write config YAML, validate, then launch.

## YAML Pattern

```yaml
model: Qwen/Qwen3-0.6B
host: "127.0.0.1"
port: 8000
dtype: auto
generation-config: vllm
max-model-len: 2048
gpu-memory-utilization: 0.9
```

Use command-line overrides intentionally because `vllm serve --config config.yaml` gives CLI args priority.
