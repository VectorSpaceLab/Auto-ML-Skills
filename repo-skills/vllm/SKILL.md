---
name: vllm
description: "Use when a user wants an agent to run vLLM offline inference, OpenAI-compatible serving, engine configuration, LoRA, structured outputs, embeddings, multimodal, distributed serving, performance tuning, benchmarking, profiling, and troubleshooting workflows from natural language using public vLLM installs and bundled helper scripts."
disable-model-invocation: true
---

# vLLM

This is the router for the vLLM repo skill. Use it to choose the focused sub-skill, then read only that sub-skill plus the linked bundled references/scripts. Do not reopen the original source checkout or depend on the inspection environment used to create this skill.

## Public Install

Prefer a clean Python 3.10-3.13 environment. For NVIDIA CUDA wheels:

```bash
python -m pip install -U pip uv
uv pip install vllm --torch-backend=auto
python -c "import importlib.metadata as m; print(m.version('vllm'))"
vllm --help
```

For a normal pip environment where PyTorch is already matched to the host accelerator:

```bash
pip install vllm
python scripts/check_env.py
```

For ROCm, TPU, Ascend, or Apple Silicon, use the public vLLM ecosystem package/image for that platform rather than a private checkout. See [references/installation.md](references/installation.md) for platform notes and the public install decision tree.

## Route To Sub-Skills

- **Offline `LLM` inference, `SamplingParams`, chat templates, batch generation, CLI `vllm chat`/`complete`/`run-batch`.**: [sub-skills/vllm-offline-inference/SKILL.md](sub-skills/vllm-offline-inference/SKILL.md)
- **OpenAI-compatible server lifecycle and `/v1/models`, chat, completions, responses, embeddings, score, health, metrics, tokenization.**: [sub-skills/vllm-openai-serving/SKILL.md](sub-skills/vllm-openai-serving/SKILL.md)
- **Serving and engine configuration: YAML config, tensor/pipeline parallel, dtype, memory, max model length, quantization, chat templates.**: [sub-skills/vllm-serving-config/SKILL.md](sub-skills/vllm-serving-config/SKILL.md)
- **LoRA adapter loading, multi-LoRA serving, runtime adapter updates, resolver plugins, adapter request payloads.**: [sub-skills/vllm-lora-adapters/SKILL.md](sub-skills/vllm-lora-adapters/SKILL.md)
- **Structured outputs, guided decoding, JSON schema, regex, choice constraints, grammar, tool calling, reasoning outputs.**: [sub-skills/vllm-structured-outputs/SKILL.md](sub-skills/vllm-structured-outputs/SKILL.md)
- **Embeddings, pooling, classification, reranking/score, offline `encode`/`score`, and OpenAI embedding-style requests.**: [sub-skills/vllm-embeddings-pooling/SKILL.md](sub-skills/vllm-embeddings-pooling/SKILL.md)
- **Multimodal image/video/audio inputs, prompt placeholders, processor kwargs, multimodal chat payloads, speech endpoints.**: [sub-skills/vllm-multimodal/SKILL.md](sub-skills/vllm-multimodal/SKILL.md)
- **Distributed serving: Ray, multiprocessing, tensor/pipeline/data parallel, expert parallel, multi-node, Kubernetes, disaggregated prefill.**: [sub-skills/vllm-distributed-serving/SKILL.md](sub-skills/vllm-distributed-serving/SKILL.md)
- **KV cache, prefix caching, chunked prefill, speculative decoding, quantized KV cache, torch compile, memory/concurrency tuning.**: [sub-skills/vllm-performance-tuning/SKILL.md](sub-skills/vllm-performance-tuning/SKILL.md)
- **Benchmarks, profiling, latency/throughput/serve/startup/mm-processor runs, benchmark result inspection.**: [sub-skills/vllm-benchmarks-profiling/SKILL.md](sub-skills/vllm-benchmarks-profiling/SKILL.md)
- **Environment checks, package/API inspection, install failures, CUDA/ROCm issues, logs, metrics, common serving and runtime errors.**: [sub-skills/vllm-observability-troubleshooting/SKILL.md](sub-skills/vllm-observability-troubleshooting/SKILL.md)

## Execution Contract

1. Resolve model, endpoint mode, output directory, accelerator, smoke/full target, and whether network/model downloads are allowed.
2. Prefer public model IDs in examples. For small text-generation smoke docs use `Qwen/Qwen3-0.6B` when available, or a caller-provided model ID; do not bake local model paths into skill outputs.
3. Read the nearest sub-skill `SKILL.md`, then one or two linked references only as needed.
4. Run bundled validation scripts first. All bundled scripts support `--help` without loading a model.
5. Launch real vLLM work through package APIs (`vllm.LLM`, `llm.generate`, `llm.chat`, `llm.encode`, `llm.score`) or package CLIs (`vllm serve`, `vllm bench`, `vllm chat`, `vllm complete`, `vllm run-batch`).
6. Manage server lifecycle explicitly: choose a free localhost port, record PID/logs, wait for `/health` or `/v1/models`, run client smoke checks, and shut down unless the user asked to keep it running.
7. Save configs, commands, request/response snippets, benchmark JSON, and logs beside the user's output artifacts.
8. Report exact artifact paths, command outcomes, and unresolved limitations such as missing GPU, model access, unsupported architecture, or long-running downloads.

## Routing Priorities

- If a request includes both server launch and payload construction, first use `vllm-serving-config` for args, then `vllm-openai-serving` for lifecycle, then the feature sub-skill for the endpoint payload.
- If a request includes both LoRA and structured output, use `vllm-lora-adapters` for model naming/server flags and `vllm-structured-outputs` for request constraints.
- If a request includes embeddings or scoring, do not route to generation-only workflows unless the user also asks for text generation.
- If a request mentions performance numbers, route to `vllm-benchmarks-profiling` for measurement and `vllm-performance-tuning` for changes after a baseline exists.
- If imports, endpoints, or CLI names are uncertain, use `vllm-observability-troubleshooting` and `scripts/inspect_api.py` before choosing version-sensitive flags.
- For distributed work, generate and validate commands before launching; multi-node side effects require explicit user intent.
- For multimodal work, validate payload/media shape before server startup because prompt placeholders and processor kwargs are model-specific.
- For all smoke tests, choose bounded token counts and deterministic parameters unless the user requests sampling behavior.

## Shared Resources

- [references/coverage-matrix.md](references/coverage-matrix.md): maps vLLM capability families to sub-skills and artifacts.
- [references/installation.md](references/installation.md): public install, platform choices, import checks, and package entrypoints.
- [references/api-surface.md](references/api-surface.md): verified public Python APIs, CLI families, and endpoint families.
- [references/model-selection.md](references/model-selection.md): model choice heuristics for small smoke tests and production sizing.
- [references/troubleshooting.md](references/troubleshooting.md): repo-wide environment, dependency, GPU, serving, and model-loading failures.
- [scripts/check_env.py](scripts/check_env.py): safe package, dependency, accelerator, and CLI inspection.
- [scripts/inspect_api.py](scripts/inspect_api.py): read-only signature/entrypoint inspection helper.
- [scripts/validate_serve_config.py](scripts/validate_serve_config.py): validates a minimal `vllm serve --config` YAML without model loading.
- [scripts/openai_client_smoke.py](scripts/openai_client_smoke.py): localhost OpenAI-compatible endpoint smoke client.
- [scripts/start_openai_server.sh](scripts/start_openai_server.sh): lifecycle helper for a short-lived `vllm serve` process.
- [scripts/vllm_skill_common.py](scripts/vllm_skill_common.py): shared helper library used by bundled scripts.

The `evals/` directory is a development artifact for self-refine checks and is not linked as runtime documentation.
