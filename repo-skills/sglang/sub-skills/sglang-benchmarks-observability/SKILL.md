---
name: sglang-benchmarks-observability
description: "Run and interpret SGLang benchmarks, profiling, Prometheus metrics, OpenTelemetry tracing, and production request logs."
disable-model-invocation: true
---

# SGLang Benchmarks And Observability

Use this sub-skill for `bench_serving`, `bench_one_batch`, profiling endpoints, Prometheus metrics, OpenTelemetry tracing, request logs, production metrics, and performance dashboards. It is the right entry point when the user asks whether a SGLang deployment is fast, saturated, observable, or comparable across revisions.

Read [references/benchmarks-observability.md](references/benchmarks-observability.md) for benchmark commands, metric names, trace/log flags, and interpretation notes. Use [scripts/validate_observability_config.py](scripts/validate_observability_config.py) to check metrics/tracing/logging flags before launching a run.

## Use When

- The user wants serving throughput, TTFT, ITL, end-to-end latency, or one-batch latency numbers.
- The user wants to compare SGLang flags, model revisions, cache policies, or hardware.
- The user wants Prometheus, OpenTelemetry, request logging, profiling, or production dashboards.
- The user has benchmark JSON/log output and needs a defensible interpretation.

## Inputs To Collect

- Model ID, server command, SGLang version, hardware, tensor/data/pipeline parallel sizes, and cache/performance flags.
- Benchmark type, request count, concurrency or request rate, input/output lengths, dataset source, tokenizer behavior, and warmup plan.
- Metrics endpoint, trace endpoint, log retention path, auth, and whether prompts may contain sensitive data.

## Workflow

1. Choose benchmark type: offline kernel/model microbenchmark, one-batch benchmark, serving benchmark, or application benchmark.
2. Record model, hardware, server args, dataset/request mix, concurrency, input/output lengths, and version.
3. Enable metrics/tracing only as needed; measure overhead separately.
4. Compare p50/p95 latency, TTFT, ITL, throughput, errors, and GPU utilization.
5. Save raw benchmark JSON/logs and the exact command before drawing conclusions.

## Verification

- Run the validator script with the planned observability flags; `--help` is safe and does not start a server.
- For a real local smoke, use a small public or user-provided model, one prompt, very low output length, and a local-only host.
- Treat multi-node benchmark results as environment-specific; require repeated runs before claiming a regression.

## Boundaries

Use `sglang-cache-performance` when the user asks which tuning flag to change. Use `sglang-openai-server` when the server has not been launched yet. Use `sglang-install-build-troubleshooting` when metrics are missing because the package, platform, or kernel import is broken.
