---
name: vllm-performance-tuning
description: "Use when a user wants vLLM KV cache, prefix caching, chunked prefill, speculative decoding, quantized KV cache, torch compile, CUDA graph, memory, throughput, latency, or scheduler tuning."
disable-model-invocation: true
---

# vLLM Performance Tuning

Use this sub-skill for performance-sensitive configuration and tuning loops.

## Short Workflow

1. Define metric target: startup, TTFT, ITL, throughput, memory, context length, or cost.
2. Capture baseline config and benchmark before changing tuning flags.
3. Read [references/workflows.md](references/workflows.md) for tuning loop.
4. Read [references/performance-reference.md](references/performance-reference.md) for feature interactions.
5. Change one factor at a time; save command, config, benchmark JSON, and environment snapshot.

## Bundled Scripts

- [scripts/make_perf_config.py](scripts/make_perf_config.py): creates a serve config with selected performance flags.
- [scripts/estimate_kv_cache.py](scripts/estimate_kv_cache.py): rough KV cache memory estimator for planning.

## References

- [references/workflows.md](references/workflows.md): tuning loop and measurement discipline.
- [references/performance-reference.md](references/performance-reference.md): prefix cache, chunked prefill, spec decode, quantized KV, compile, and memory notes.

## Boundaries

Use `vllm-benchmarks-profiling` for benchmark execution details and `vllm-serving-config` for base engine args.
