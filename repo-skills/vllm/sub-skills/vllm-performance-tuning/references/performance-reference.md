# Performance Reference

## Prefix Caching

Prefix caching improves repeated-prefix workloads. It may be unsupported or experimental for some model classes. Enable only after confirming correctness for the target model.

## Chunked Prefill

Chunked prefill can improve scheduling under mixed prompt lengths. It interacts with long-context and multimodal workloads.

## Speculative Decoding

Speculative decoding uses a draft model or draft method to accelerate decode. Validate quality and throughput with the exact workload; speedups are workload-dependent.

## Quantized KV Cache

Quantized KV cache reduces memory pressure but may change accuracy/performance. Benchmark before production use.

## Compile/CUDA Graphs

Compilation and CUDA graph behavior can improve steady-state performance but may increase startup time or memory. Compare cold and warm performance separately.
