# SGLang Coverage Matrix

| Capability | Sub-skill | Bundled detail | Scripts | Depth |
| --- | --- | --- | --- | --- |
| Offline Runtime/Engine generation, language frontend, native `/generate`, sampling params | `sglang-offline-runtime` | `references/offline-runtime.md` | `scripts/run_offline_smoke.py` | API signatures checked; examples distilled from runtime docs/examples and installed package imports. |
| OpenAI-compatible serving and lifecycle | `sglang-openai-server` | `references/openai-server.md` | `scripts/server_helper.py`, `scripts/openai_client_smoke.py` | HTTP routes inspected from server source; script validates health/models/chat/completions; Responses routes are documented separately. |
| Router, TP/DP/PP/EP, multi-node, PD disaggregation | `sglang-distributed-topology` | `references/distributed-topology.md` | `scripts/validate_topology.py` | ServerArgs and router args inspected; launch plans are config-validated, not cluster-executed. |
| Structured outputs and constrained decoding | `sglang-structured-outputs` | `references/structured-outputs.md` | `scripts/validate_constraints.py` | SamplingParams and frontend `gen/select` inspected; JSON/regex/EBNF exclusivity encoded. |
| Multimodal inputs, VLM serving, ASR, diffusion CLI/server | `sglang-multimodal-serving` | `references/multimodal-serving.md` | `scripts/validate_multimodal_payload.py` | Server endpoints and docs/examples inspected for image/video/audio; payload validator is local-only. |
| Tool use, function calling, Responses tools, reasoning parser, chat templates | `sglang-tool-reasoning` | `references/tool-reasoning.md` | `scripts/validate_tool_payload.py` | Parser flags/env and OpenAI payload structure distilled; parser availability depends on installed build. |
| Embedding, classify, score, rerank, reward models | `sglang-embeddings-rerank-score` | `references/embeddings-rerank-score.md` | `scripts/validate_retrieval_payload.py` | HTTP routes `/v1/embeddings`, `/v1/classify`, `/v1/score`, `/v1/rerank` inspected. |
| LoRA adapters and weight updates | `sglang-lora-weight-updates` | `references/lora-weight-updates.md` | `scripts/validate_lora_payload.py` | ServerArgs LoRA fields and HTTP adapter/weight routes inspected. |
| Cache, HiCache, RadixAttention, speculative decoding, performance flags | `sglang-cache-performance` | `references/cache-performance.md` | `scripts/validate_perf_config.py` | Advanced docs, ServerArgs fields, env vars, and examples inspected; script catches incompatible options. |
| Benchmarks, profiling, metrics, tracing | `sglang-benchmarks-observability` | `references/benchmarks-observability.md` | `scripts/validate_observability_config.py` | Benchmark modules, profile endpoints, Prometheus/OpenTelemetry docs inspected. |
| Install/build/platform/kernel troubleshooting | `sglang-install-build-troubleshooting` | `references/install-build-troubleshooting.md` | `scripts/check_install.py` | Install docs, pyproject dependencies/extras, environment variable docs, platform docs inspected. |

Creation validation included:

- Repository metadata/docs/examples/tests/CLI/API inspection.
- Installed package import/signature checks for `sglang`, `RuntimeEndpoint`, `function`, `gen`, `select`, and package version.
- HTTP server route inspection for native, OpenAI-compatible, LoRA, weight update, profile, HiCache, and cloud compatibility routes.
- Router argument source inspection for policy, service discovery, PD disaggregation, health, metrics, auth, parser, and TLS options.

Known limits:

- The bundled scripts avoid heavy GPU/model loads unless explicitly invoked with model/server arguments.
- Multi-node, router, and disaggregation examples are validated structurally; real deployment still depends on cluster networking, ports, and hardware.
- Diffusion and advanced kernel workflows are covered operationally, but custom model/kernel development may require reading current upstream code outside this public-ready skill.
