---
name: sglang-cache-performance
description: "Tune SGLang prefix cache, RadixAttention, HiCache, chunked prefill, speculative decoding, quantization, and performance settings."
disable-model-invocation: true
---

# SGLang Cache And Performance

Use this sub-skill for prefix cache/RadixAttention, HiCache, chunked prefill, speculative decoding, quantization, attention/kernel backend selection, memory tuning, and throughput/latency tradeoffs.

Read [references/cache-performance.md](references/cache-performance.md). Use [scripts/validate_perf_config.py](scripts/validate_perf_config.py) for quick config sanity checks.

## Workflow

1. Establish workload shape: prompt length, output length, concurrency, repeated prefixes, model architecture, and target latency/throughput.
2. Tune memory first (`mem_fraction_static`, token limits, chunked prefill), then cache policy, then speculative/quantization/kernel backends.
3. Validate one setting change at a time with benchmark/observability tooling.
4. For multi-node or PD cache behavior, combine with `sglang-distributed-topology`.
