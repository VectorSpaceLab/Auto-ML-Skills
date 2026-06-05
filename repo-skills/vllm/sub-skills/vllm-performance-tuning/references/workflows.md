# Performance Tuning Workflow

1. Capture baseline command/config and environment.
2. Run a benchmark or representative request set.
3. Identify bottleneck: startup, TTFT, decode latency, throughput, memory, or preprocessing.
4. Change one option at a time.
5. Re-run the same benchmark and compare JSON metrics.
6. Keep a log of changes and rollback if quality or stability regresses.

## Common First Moves

- Memory OOM: reduce `max-model-len`, lower concurrency, use smaller model or quantized weights.
- Long TTFT: check prefix caching, chunked prefill, prompt length, and prefill concurrency.
- Slow decode: check speculative decoding, tensor parallel overhead, quantization backend, and batch size.
- Startup slow: check model download/cache, compilation, and warmup.
