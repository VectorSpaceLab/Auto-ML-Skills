# vLLM Coverage Matrix

| Capability family | Sub-skill | References | Scripts | Depth |
|---|---|---|---|---|
| Offline `LLM` generation, `SamplingParams`, chat templates, batch generation | `vllm-offline-inference` | `references/workflows.md`, `references/cli-reference.md` | `run_offline_smoke.py`, `make_batch_requests.py` | Deep |
| OpenAI-compatible server, chat/completions/responses/embeddings/models/health/metrics | `vllm-openai-serving` | `references/workflows.md`, `references/endpoints.md` | `start_server.py`, `client_smoke.py` | Deep |
| Engine/server args, YAML config, tensor parallel, dtype, max model len, quantization | `vllm-serving-config` | `references/workflows.md`, `references/engine-args.md` | `make_serve_config.py`, `validate_config.py` | Deep |
| LoRA/multi-LoRA/runtime adapters/resolver plugins | `vllm-lora-adapters` | `references/workflows.md`, `references/lora-reference.md` | `make_lora_payload.py`, `validate_lora_config.py` | Deep |
| Structured outputs/guided decoding/JSON/regex/grammar/tool calls/reasoning | `vllm-structured-outputs` | `references/workflows.md`, `references/guided-decoding.md` | `make_structured_payload.py`, `validate_schema.py` | Deep |
| Embeddings/pooling/classification/reranking/score | `vllm-embeddings-pooling` | `references/workflows.md`, `references/pooling-reference.md` | `make_embedding_payload.py`, `score_payload.py` | Deep |
| Multimodal image/video/audio/speech payloads and processor kwargs | `vllm-multimodal` | `references/workflows.md`, `references/multimodal-reference.md` | `make_mm_payload.py`, `validate_media_payload.py` | Medium |
| Distributed serving, Ray, multiproc, TP/PP/DP/EP, multi-node, K8s, disaggregated prefill | `vllm-distributed-serving` | `references/workflows.md`, `references/distributed-reference.md` | `make_distributed_command.py`, `check_cluster_env.py` | Medium |
| KV cache, prefix caching, chunked prefill, speculative decoding, quantized KV, compile | `vllm-performance-tuning` | `references/workflows.md`, `references/performance-reference.md` | `make_perf_config.py`, `estimate_kv_cache.py` | Deep |
| Benchmarks/profiling/latency/throughput/serve/startup/mm-processor/sweeps | `vllm-benchmarks-profiling` | `references/workflows.md`, `references/benchmark-reference.md` | `make_benchmark_command.py`, `inspect_benchmark_json.py` | Deep |
| Environment/observability/troubleshooting/logs/metrics/import/API inspection | `vllm-observability-troubleshooting` | `references/workflows.md`, `references/troubleshooting-playbook.md` | `check_env.py`, `collect_report.py` | Deep |

## Cross-Cutting Root Artifacts

- `references/installation.md`: public install and platform decision tree.
- `references/api-surface.md`: public API, CLI, and endpoint summary.
- `references/model-selection.md`: public model selection and sizing heuristics.
- `references/troubleshooting.md`: repo-wide failures.
- `scripts/check_env.py`: safe environment inspection.
- `scripts/inspect_api.py`: public package signature and entrypoint inspection.
- `scripts/validate_serve_config.py`: general YAML config validation.
- `scripts/start_openai_server.sh`: server lifecycle wrapper.
- `scripts/openai_client_smoke.py`: endpoint smoke client.

## Known Limits

- The skill cannot guarantee model architecture support for every new Hugging Face model; use `inspect_api.py`, vLLM error output, and a small smoke run.
- Some structured-output, tool parser, score, speech, or multimodal features vary by vLLM version and model family; validate request schemas in the installed package.
- Multi-node, K8s, and Ray Serve commands are environment-dependent. The sub-skill provides command generation and checks, not a universal cluster bootstrap.
