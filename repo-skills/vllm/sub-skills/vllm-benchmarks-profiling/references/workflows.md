# Benchmark And Profiling Workflow

## Benchmark Selection

- `vllm bench latency`: local model latency.
- `vllm bench throughput`: local engine throughput.
- `vllm bench serve`: HTTP serving benchmark against a running endpoint.
- `vllm bench startup`: startup timing.
- `vllm bench mm-processor`: multimodal processor latency.
- `vllm bench sweep`: parameter sweeps.

## Procedure

1. Save environment report and exact model ID.
2. Generate a small command with `scripts/make_benchmark_command.py`.
3. Run a tiny smoke benchmark first.
4. Scale prompts/request rate/context lengths.
5. Save JSON output and logs.
6. Inspect JSON with `scripts/inspect_benchmark_json.py`.

## Profiling

Use vLLM profiling flags/routes only after server startup and workload are reproducible. Keep profiler duration short and avoid mixing profiler runs with headline benchmark results.
