---
name: vllm-benchmarks-profiling
description: "Use when a user wants vLLM benchmark or profiling workflows, including bench latency, throughput, serve, startup, mm-processor, sweeps, profiling logs, and benchmark JSON inspection."
disable-model-invocation: true
---

# vLLM Benchmarks And Profiling

Use this sub-skill for repeatable benchmark commands, profiling setup, and result inspection. It is the right entry point when the user needs evidence about vLLM throughput, TTFT, ITL, latency, startup cost, failed requests, or performance regressions.

## Use When

- The user wants `vllm bench latency`, `vllm bench throughput`, `vllm bench serve`, startup benchmarks, multimodal processor benchmarks, or benchmark sweeps.
- The user has benchmark JSON/logs and needs to interpret metrics or compare runs.
- The user wants profiling artifacts, request traces, or a repeatable benchmark plan before tuning.
- The user asks whether a config change improved performance.

## Inputs To Collect

- Model ID, vLLM version, hardware, server command, engine args, quantization, max model length, and parallelism.
- Benchmark type, dataset/request source, prompt/output lengths, request count, concurrency/RPS, warmup, random seed, and output directory.
- Whether the server is already running, whether prompts may contain private data, and which metric is the target.

## Short Workflow

1. Choose benchmark type: `latency`, `throughput`, `serve`, `startup`, `mm-processor`, or `sweep`.
2. Read [references/workflows.md](references/workflows.md) for benchmark setup and artifact capture.
3. Read [references/benchmark-reference.md](references/benchmark-reference.md) for dataset choices and metrics.
4. Create a small dry-run command first, then scale num-prompts/RPS/output length.
5. Inspect benchmark JSON for failed requests and metric names before comparing runs.
6. Keep the baseline command and changed command side by side; compare only runs with matching workload shape.

## Bundled Scripts

- [scripts/make_benchmark_command.py](scripts/make_benchmark_command.py): generates a `vllm bench ...` command.
- [scripts/inspect_benchmark_json.py](scripts/inspect_benchmark_json.py): summarizes benchmark JSON files.

## References

- [references/workflows.md](references/workflows.md): benchmark/profiling workflow.
- [references/benchmark-reference.md](references/benchmark-reference.md): CLI families, datasets, metrics, and pitfalls.

## Boundaries

Use `vllm-performance-tuning` for tuning decisions and `vllm-openai-serving` for server lifecycle before `bench serve`.

## Verification Notes

- The command generator and JSON inspector can be run without loading a model.
- A real benchmark requires a live model/server or local model load; record that separately from static command generation.
- Do not claim distributed or production performance was validated unless the actual target topology was benchmarked.
