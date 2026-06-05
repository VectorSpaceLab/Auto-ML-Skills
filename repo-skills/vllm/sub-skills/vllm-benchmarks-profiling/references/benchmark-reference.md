# Benchmark Reference

## Metrics To Capture

- Request throughput.
- Output token throughput.
- Total token throughput.
- Time to first token (TTFT).
- Inter-token latency (ITL).
- End-to-end latency.
- Failed request count.
- Startup time for startup benchmarks.

## Dataset Choices

- Random dataset for synthetic smoke.
- ShareGPT-like datasets for chat workloads.
- Custom JSONL/text slices for workload-specific testing.
- Multimodal datasets for media processing benchmarks.

## Pitfalls

- Compare warm runs separately from cold starts.
- Failed requests invalidate throughput comparisons.
- Client and server must agree on model name and endpoint type.
- RPS sweeps can overload the server; ramp gradually.
- Record `max_tokens`, prompt length, concurrency, and server args with every result.
