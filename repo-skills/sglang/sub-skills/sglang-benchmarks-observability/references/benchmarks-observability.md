# Benchmarks And Observability Reference

## Benchmarks

Common benchmark surfaces:

- `python -m sglang.bench_one_batch` for local model/attention/kernel style checks.
- `python -m sglang.bench_offline_throughput` for offline throughput.
- Serving benchmark tooling for HTTP throughput/latency.
- Application benchmarks in repository examples cover MMLU, GSM8K, HellaSwag, MT-Bench, JSON decoding, multimodal, LoRA, HiCache, and long-context cases.

Benchmark plans should specify:

- Model ID and dtype/quantization.
- GPU/node topology and server args.
- Prompt/output length distribution.
- Concurrency, request rate, duration, warmup.
- Streaming/non-streaming and OpenAI/native endpoint.

## Profiling

Inspected control routes:

- `/start_profile`
- `/stop_profile`
- `/set_trace_level`
- expert distribution record start/stop/dump routes.

Environment variables include profiler output directory and torch profiler stack/shape settings. Use profiling for short windows; it can affect performance.

## Metrics

Server flags:

- `--enable-metrics`
- `--enable-mfu-metrics`
- `--enable-metrics-for-all-schedulers`
- metric bucket flags for TTFT, inter-token latency, end-to-end latency, prompt tokens, and generation tokens.
- `--extra-metric-labels`.

Router flags include Prometheus host/port and duration buckets.

## Tracing

Server/router tracing:

```bash
python -m sglang.launch_server --model-path <MODEL_ID> --enable-trace --otlp-traces-endpoint <HOST>:4317
python -m sglang_router.launch_router --enable-trace --otlp-traces-endpoint <HOST>:4317
```

For HTTP/protobuf exporters, configure the OpenTelemetry protocol environment in the runtime environment. Trace levels can be adjusted through env or `/set_trace_level`.

## Request Logs

Use `--log-requests`, `--log-requests-level`, `--log-requests-format`, and `--log-requests-target`. Avoid logging prompts containing secrets or user data in production unless retention/redaction is configured.
