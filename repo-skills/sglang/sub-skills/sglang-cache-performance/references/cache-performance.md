# Cache And Performance Reference

## Prefix Cache And RadixAttention

SGLang emphasizes RadixAttention/prefix caching for repeated prompt prefixes. Relevant controls include:

- `--disable-radix-cache` when debugging cache effects.
- `--radix-eviction-policy` with policies such as `lru`, `lfu`, `slru`, `priority`.
- `/flush_cache` to clear prefix cache.
- `SGLANG_CHUNKED_PREFIX_CACHE_THRESHOLD`.

Use cache-aware routing when multiple workers serve repeated-prefix traffic.

## Chunked Prefill And Scheduler

Common controls:

- `--chunked-prefill-size`.
- `--enable-dynamic-chunking`.
- `--max-prefill-tokens`.
- `--prefill-max-requests`.
- `--schedule-policy`.
- `--schedule-conservativeness`.
- `--max-running-requests`, `--max-queued-requests`, `--max-total-tokens`.

Chunked prefill helps long prompts and mixed workloads, but can increase time-to-first-token if over-sliced.

## HiCache

Routes:

- `POST /hicache/storage-backend/clear`
- `PUT /hicache/storage-backend`
- `DELETE /hicache/storage-backend`
- `GET /hicache/storage-backend`

HiCache storage/runtime settings are useful for long-context and repeated-context workloads. Validate storage backend config and offload stride before production use.

## Speculative Decoding

Relevant ServerArgs:

- `--speculative-algorithm`.
- `--speculative-draft-model-path`.
- `--speculative-num-steps`.
- `--speculative-eagle-topk`.
- `--speculative-num-draft-tokens`.
- `--speculative-draft-attention-backend`.
- `--speculative-draft-model-quantization`.
- N-gram and EAGLE/NEXTN variants depending on model support.

Speculative decoding requires a compatible draft strategy/model. Benchmark acceptance rate and output quality.

## Quantization And Kernels

Quantization choices include AWQ, FP8, MXFP8, GPTQ, Marlin variants, bitsandbytes, GGUF, ModelOpt variants, NVFP4/MXFP4, compressed-tensors, MLX quantization, and platform-specific choices.

Attention/backend knobs include:

- `--attention-backend`, `--decode-attention-backend`, `--prefill-attention-backend`.
- `--sampling-backend`.
- `--fp8-gemm-runner-backend`, `--fp4-gemm-runner-backend`.
- `--moe-runner-backend`, `--moe-a2a-backend`.

Prefer defaults until a benchmark shows bottleneck or hardware-specific docs recommend a backend.

## Practical Tuning Order

1. Verify model loads and single request correctness.
2. Set concurrency and memory caps.
3. Benchmark baseline throughput/latency.
4. Enable/tune prefix cache and chunked prefill.
5. Add quantization or speculative decoding.
6. Turn on metrics/tracing and compare.
