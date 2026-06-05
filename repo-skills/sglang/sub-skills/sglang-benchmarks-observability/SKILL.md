---
name: sglang-benchmarks-observability
description: "Run and interpret SGLang benchmarks, profiling, Prometheus metrics, OpenTelemetry tracing, and production request logs."
disable-model-invocation: true
---

# SGLang Benchmarks And Observability

Use this sub-skill for `bench_serving`, `bench_one_batch`, profiling endpoints, Prometheus metrics, OpenTelemetry tracing, request logs, production metrics, and performance dashboards.

Read [references/benchmarks-observability.md](references/benchmarks-observability.md). Use [scripts/validate_observability_config.py](scripts/validate_observability_config.py) to check metrics/tracing/logging flags.

## Workflow

1. Choose benchmark type: offline kernel/model microbenchmark, one-batch benchmark, serving benchmark, or application benchmark.
2. Record model, hardware, server args, dataset/request mix, concurrency, input/output lengths, and version.
3. Enable metrics/tracing only as needed; measure overhead separately.
4. Compare p50/p95 latency, TTFT, ITL, throughput, errors, and GPU utilization.
