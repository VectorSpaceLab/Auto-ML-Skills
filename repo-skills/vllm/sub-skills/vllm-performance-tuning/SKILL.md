---
name: vllm-performance-tuning
description: "Use when a user wants vLLM KV cache, prefix caching, chunked prefill, speculative decoding, quantized KV cache, torch compile, CUDA graph, memory, throughput, latency, or scheduler tuning."
disable-model-invocation: true
---

# vLLM Performance Tuning

Use this sub-skill for performance-sensitive configuration and tuning loops. It covers KV cache, prefix caching, chunked prefill, speculative decoding, quantized KV cache, torch compile, CUDA graphs, memory sizing, scheduler behavior, throughput, latency, and cost tradeoffs.

## Use When

- The user wants to improve throughput, TTFT, ITL, latency, memory use, context length, startup time, or GPU utilization.
- The user mentions prefix caching, chunked prefill, speculative decoding, KV cache dtype, CUDA graph, torch compile, scheduler flags, or quantization.
- The user has a correct vLLM server/offline workflow and now wants to tune it.
- The user asks for a benchmark-backed tuning plan rather than a one-off flag guess.

## Inputs To Collect

- Baseline command/config, model, hardware, max model length, concurrency, prompt/output length distribution, quantization, and memory budget.
- Target metric and acceptable tradeoffs for startup time, determinism, quality, latency, and throughput.
- Benchmark output, server logs, and whether changes must be reversible.

## Short Workflow

1. Define metric target: startup, TTFT, ITL, throughput, memory, context length, or cost.
2. Capture baseline config and benchmark before changing tuning flags.
3. Read [references/workflows.md](references/workflows.md) for tuning loop.
4. Read [references/performance-reference.md](references/performance-reference.md) for feature interactions.
5. Change one factor at a time; save command, config, benchmark JSON, and environment snapshot.
6. Roll back any change that improves one metric while violating correctness, memory, or latency constraints.

## Bundled Scripts

- [scripts/make_perf_config.py](scripts/make_perf_config.py): creates a serve config with selected performance flags.
- [scripts/estimate_kv_cache.py](scripts/estimate_kv_cache.py): rough KV cache memory estimator for planning.

## References

- [references/workflows.md](references/workflows.md): tuning loop and measurement discipline.
- [references/performance-reference.md](references/performance-reference.md): prefix cache, chunked prefill, spec decode, quantized KV, compile, and memory notes.

## Boundaries

Use `vllm-benchmarks-profiling` for benchmark execution details and `vllm-serving-config` for base engine args.

## Verification Notes

- Config generation and KV estimates are planning aids, not runtime proof.
- A real performance claim requires at least baseline and changed benchmark runs with the same workload.
- Do not generalize a Qwen short-prompt smoke into long-context or production throughput claims.
