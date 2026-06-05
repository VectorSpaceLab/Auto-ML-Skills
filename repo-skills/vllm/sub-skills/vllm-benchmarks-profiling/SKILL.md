---
name: vllm-benchmarks-profiling
description: "Use when a user wants vLLM benchmark or profiling workflows, including bench latency, throughput, serve, startup, mm-processor, sweeps, profiling logs, and benchmark JSON inspection."
disable-model-invocation: true
---

# vLLM Benchmarks And Profiling

Use this sub-skill for repeatable benchmark commands, profiling setup, and result inspection.

## Short Workflow

1. Choose benchmark type: `latency`, `throughput`, `serve`, `startup`, `mm-processor`, or `sweep`.
2. Read [references/workflows.md](references/workflows.md) for benchmark setup and artifact capture.
3. Read [references/benchmark-reference.md](references/benchmark-reference.md) for dataset choices and metrics.
4. Create a small dry-run command first, then scale num-prompts/RPS/output length.
5. Inspect benchmark JSON for failed requests and metric names before comparing runs.

## Bundled Scripts

- [scripts/make_benchmark_command.py](scripts/make_benchmark_command.py): generates a `vllm bench ...` command.
- [scripts/inspect_benchmark_json.py](scripts/inspect_benchmark_json.py): summarizes benchmark JSON files.

## References

- [references/workflows.md](references/workflows.md): benchmark/profiling workflow.
- [references/benchmark-reference.md](references/benchmark-reference.md): CLI families, datasets, metrics, and pitfalls.

## Boundaries

Use `vllm-performance-tuning` for tuning decisions and `vllm-openai-serving` for server lifecycle before `bench serve`.
