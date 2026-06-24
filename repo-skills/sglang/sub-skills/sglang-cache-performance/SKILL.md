---
name: sglang-cache-performance
description: "Tune SGLang prefix cache, RadixAttention, HiCache, chunked prefill, speculative decoding, quantization, and performance settings."
disable-model-invocation: true
---

# SGLang Cache And Performance

Use this sub-skill for prefix cache/RadixAttention, HiCache, chunked prefill, speculative decoding, quantization, attention/kernel backend selection, memory tuning, and throughput/latency tradeoffs. It owns the decision loop for changing SGLang performance flags after a baseline request already works.

Read [references/cache-performance.md](references/cache-performance.md) for the actual flag families and gotchas. Use [scripts/validate_perf_config.py](scripts/validate_perf_config.py) for quick config sanity checks before running a benchmark.

## Use When

- The user wants better throughput, lower TTFT/ITL, lower memory, longer context, or higher concurrency.
- The user mentions prefix cache, RadixAttention, HiCache, chunked prefill, speculative decoding, quantization, CUDA graphs, or kernel backends.
- The user has a working server but performance is unstable or worse than expected.
- The user needs to decide whether a tuning feature is compatible with the model/hardware/workload.

## Inputs To Collect

- Prompt length distribution, output length distribution, concurrency, repeated-prefix ratio, streaming needs, and latency target.
- Model architecture, quantization, context length, available GPU memory, visible GPUs, and existing server args.
- Baseline benchmark command/output and whether quality equivalence must be checked after tuning.

## Workflow

1. Establish workload shape: prompt length, output length, concurrency, repeated prefixes, model architecture, and target latency/throughput.
2. Tune memory first (`mem_fraction_static`, token limits, chunked prefill), then cache policy, then speculative/quantization/kernel backends.
3. Validate one setting change at a time with benchmark/observability tooling.
4. For multi-node or PD cache behavior, combine with `sglang-distributed-topology`.
5. Keep an explicit rollback command for each feature flag.

## Verification

- Start from a known-good single prompt smoke before tuning.
- Use `sglang-benchmarks-observability` for p50/p95, TTFT, ITL, throughput, and error-rate evidence.
- Do not claim a tuning win from one run; compare at least baseline versus changed config with the same dataset and output length.

## Boundaries

Use `sglang-openai-server` for lifecycle and endpoint smoke. Use `sglang-distributed-topology` for router, PD, EP, and multi-node arithmetic. Use `sglang-install-build-troubleshooting` when a backend flag fails due to missing kernels or platform packages.
