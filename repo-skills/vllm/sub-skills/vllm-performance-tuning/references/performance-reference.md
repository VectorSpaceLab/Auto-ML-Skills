# Performance Reference

## Prefix Caching

Prefix caching improves repeated-prefix workloads and is usually a serving-level latency optimization, not a model-quality feature. Enable it with `--enable-prefix-caching` or YAML `enable-prefix-caching: true`, then test repeated prompts with identical leading tokens. If privacy isolation matters, use request-level cache salting where supported by the installed version.

## Chunked Prefill

Chunked prefill can improve scheduling under mixed prompt lengths. It interacts with long-context, prefix caching, multimodal placeholder expansion, and TTFT/throughput tradeoffs. Keep `max-model-len`, batch size, and request shape fixed when measuring it.

## Speculative Decoding

Speculative decoding uses a draft model or draft method to accelerate decode. Common public flags are:

- `--speculative-config '<json>'` for the full version-specific config.
- `--spec-model <draft_model>` and `--spec-tokens <n>` for a draft model path/ID.
- `--spec-method <method>` for built-in methods where available, such as n-gram or EAGLE-style variants.

Validate quality and throughput with the exact workload; speedups are workload-dependent. Spec decode can increase KV cache pressure because vLLM may reserve extra slots for proposed tokens. If a small smoke fails with a capacity error, reduce `--spec-tokens`, `max-num-seqs`, `max-model-len`, or GPU memory use before assuming the model is unsupported.

## Quantized KV Cache

Quantized KV cache reduces memory pressure but may change accuracy/performance. Typical flags:

- `--kv-cache-dtype fp8`, `fp8_e4m3`, or `fp8_e5m2` where the backend supports it.
- `--calculate-kv-scales` when runtime scale calculation is needed and supported.
- `--kv-cache-dtype-skip-layers` for model-specific exceptions.

For prefill/decode disaggregation, producers and consumers must use compatible cache dtype and layout. Static checkpoint scales are easier to reason about than dynamic runtime scales.

## Weight Quantization

Weight quantization is configured separately from KV cache quantization. `--quantization` must match the model artifact and installed backend. Common families include `awq`, `gptq`, `gptqmodel`, `bitsandbytes`, `gguf`, `fp8`, `compressed-tensors`, `modelopt`, `torchao`, `inc`, and `quark`. Always start from the model card or artifact format; do not add `--quantization` to an arbitrary dense checkpoint.

## Compile/CUDA Graphs

Compilation and CUDA graph behavior can improve steady-state performance but may increase startup time or memory. Compare cold and warm performance separately. Use `--compilation-config '<json>'`, `--optimization-level`, or `--performance-mode` when the installed CLI exposes them. CUDA graph capture is sensitive to shapes, multimodal inputs, and memory headroom; use `--enforce-eager` only as a diagnostic or when capture/compile fails.

## Dual Batch Overlap

Dual batch overlap (DBO) overlaps decode and prefill microbatches. Use it only after a baseline:

```bash
vllm serve MODEL --enable-dbo \
  --dbo-decode-token-threshold 32 \
  --dbo-prefill-token-threshold 512
```

Tune thresholds against TTFT, inter-token latency, and throughput. DBO changes scheduling behavior, so compare with the same traffic mix and concurrency.

## Measurement Discipline

- Take a baseline with no optional feature flags.
- Add one change at a time.
- Record model, tokenizer/chat template, vLLM version, GPU count, dtype, quantization, `max-model-len`, request lengths, concurrency, and benchmark JSON.
- Treat startup time, first request latency, warm steady-state throughput, and tail latency as separate metrics.
