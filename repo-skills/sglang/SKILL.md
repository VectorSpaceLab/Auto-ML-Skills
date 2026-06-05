---
name: sglang
description: "Route SGLang serving, offline inference, structured output, multimodal, LoRA, distributed, cache, benchmark, and troubleshooting tasks to focused repo sub-skills."
disable-model-invocation: true
---

# SGLang Repo Skill

This is the router for the SGLang repo skill. Use it to choose the nearest focused sub-skill, then read only that sub-skill plus the linked references/scripts. Do not require the original source checkout, the inspection virtualenv, or any local model path used when this skill was created.

Public examples should use public model IDs or placeholders. For lightweight smoke examples, prefer a public small model such as `Qwen/Qwen3-0.6B` when suitable, or use `<MODEL_ID>` when the user has not chosen a model.

## Routing

- Offline generation, Engine/Runtime API, SGLang language frontend, native `/generate`, sampling params, chat-template use in local code: use [sub-skills/sglang-offline-runtime/SKILL.md](sub-skills/sglang-offline-runtime/SKILL.md).
- OpenAI-compatible server lifecycle, `/v1/chat/completions`, `/v1/completions`, `/v1/models`, `/health`, `/generate`, API keys, curl/OpenAI clients: use [sub-skills/sglang-openai-server/SKILL.md](sub-skills/sglang-openai-server/SKILL.md).
- Tensor/data/pipeline parallelism, multi-node serving, router/model gateway, Kubernetes, prefill-decode disaggregation: use [sub-skills/sglang-distributed-topology/SKILL.md](sub-skills/sglang-distributed-topology/SKILL.md).
- JSON schema, regex, EBNF, structural tags, constrained decoding, choices/select, grammar backends: use [sub-skills/sglang-structured-outputs/SKILL.md](sub-skills/sglang-structured-outputs/SKILL.md).
- Vision-language, image/audio/video request payloads, multimodal embeddings, diffusion/image generation CLI/server: use [sub-skills/sglang-multimodal-serving/SKILL.md](sub-skills/sglang-multimodal-serving/SKILL.md).
- Function calling, tool-call parsers, reasoning parser, thinking separation, chat template parser issues: use [sub-skills/sglang-tool-reasoning/SKILL.md](sub-skills/sglang-tool-reasoning/SKILL.md).
- Embeddings, rerank, classify, score, reward models, prefill-only scoring endpoints: use [sub-skills/sglang-embeddings-rerank-score/SKILL.md](sub-skills/sglang-embeddings-rerank-score/SKILL.md).
- LoRA adapters, multi-LoRA serving, adapter load/unload, `lora_path`, weight updates, RL/post-training weight sync: use [sub-skills/sglang-lora-weight-updates/SKILL.md](sub-skills/sglang-lora-weight-updates/SKILL.md).
- Prefix cache/RadixAttention, HiCache, chunked prefill, speculative decoding, quantization/performance flags: use [sub-skills/sglang-cache-performance/SKILL.md](sub-skills/sglang-cache-performance/SKILL.md).
- Benchmarks, profiling, Prometheus metrics, OpenTelemetry tracing, request logs, production metrics: use [sub-skills/sglang-benchmarks-observability/SKILL.md](sub-skills/sglang-benchmarks-observability/SKILL.md).
- Install/build, CUDA/ROCm/CPU/XPU/NPU/TPU platform checks, custom kernels, environment variables, import failures: use [sub-skills/sglang-install-build-troubleshooting/SKILL.md](sub-skills/sglang-install-build-troubleshooting/SKILL.md).

## Default Workflow

1. Clarify the user's target surface: offline Python, native HTTP, OpenAI-compatible HTTP, router, multimodal, adapter/weights, or performance/debugging.
2. Load the focused sub-skill and its linked reference. Avoid loading multiple sub-skills unless the request crosses boundaries, such as a multimodal OpenAI server with LoRA.
3. Prefer deterministic helper scripts for validation before writing new command snippets. All bundled scripts support `--help` without loading a model or requiring a GPU.
4. When launching a real server, choose a free port, document the model ID, record the PID, validate `/health` or `/v1/models`, and stop the server unless the user explicitly wants it left running.
5. For public-ready examples, never write local paths, private tokens, or host-specific package locations into generated commands.

## Global References And Scripts

- [references/coverage-matrix.md](references/coverage-matrix.md): maps SGLang capability families to sub-skills, references, scripts, and validation depth.
- [references/model-selection.md](references/model-selection.md): public model IDs and placeholders for smoke docs.
- [scripts/check_env.py](scripts/check_env.py): lightweight environment/import/device/package probe.
- [scripts/inspect_api.py](scripts/inspect_api.py): inspect installed SGLang API, CLI entrypoints, and selected signatures.
- [scripts/validate_no_local_paths.py](scripts/validate_no_local_paths.py): audit generated commands/docs for source, env, or local model path leaks.

## Cross-Cutting Requests

- OpenAI server plus structured outputs: load `sglang-openai-server` first for lifecycle and endpoint choice, then `sglang-structured-outputs` for schema/grammar validation.
- OpenAI server plus tools/reasoning: load `sglang-tool-reasoning` after server basics; parser flags affect how chat templates and tool calls are interpreted.
- Multimodal plus embeddings: load `sglang-multimodal-serving` for payload shape and `sglang-embeddings-rerank-score` for `/v1/embeddings` or `/encode`.
- Distributed plus performance: load `sglang-distributed-topology` for rank/router shape, then `sglang-cache-performance` for cache/speculative/quantization knobs.
- Production diagnostics: load `sglang-benchmarks-observability` and, if imports or kernels fail, `sglang-install-build-troubleshooting`.
- LoRA plus OpenAI chat: load `sglang-lora-weight-updates` for adapter lifecycle and `sglang-openai-server` for client smoke.

## Validation Ladder

1. Static plan: use the nearest sub-skill reference and validator script with `--help` or dry-run options.
2. Environment check: run `scripts/check_env.py` when package/device state matters.
3. API inspection: run `scripts/inspect_api.py` to confirm installed signatures before relying on optional surfaces.
4. Server check: start a managed server only when a model and hardware are available; validate `/health` and `/v1/models`.
5. Functional smoke: send one minimal request on the exact endpoint the user will use.
6. Cleanup: stop managed processes and remove temporary payload files or pid files unless the user asks to keep them.

## Public Example Policy

- Keep examples runnable from a normal package install; do not reference source checkout files.
- Prefer public Hugging Face IDs, but keep `<MODEL_ID>` when hardware, license, or modality is uncertain.
- Do not include private auth tokens; show environment variable placeholders such as `<HF_TOKEN>` only when needed.
- Keep local adapter/model paths out of reusable docs. They can appear only in task-specific commands if the user provided them.
- Include `--host 127.0.0.1` for local smoke and `--host 0.0.0.0` only when explaining deployment.
- State when a script is structural-only versus actually loading a model.

## Command Conventions

- Server launch: `python -m sglang.launch_server --model-path <MODEL_ID> --host 127.0.0.1 --port 30000`.
- CLI equivalent: `sglang serve --model-path <MODEL_ID> --host 127.0.0.1 --port 30000`.
- OpenAI base URL: `http://127.0.0.1:30000/v1`; native endpoint base URL: `http://127.0.0.1:30000`.
- Use `--api-key <KEY>` when exposing any non-local server. For local examples without auth, OpenAI clients can pass `api_key="None"`.
- Common small public model placeholder: `Qwen/Qwen3-0.6B`; use a larger instruction or multimodal model only when the requested feature requires it.

## Safety Notes

- Do not start long-running servers without a shutdown path. Prefer the sub-skill server helper for smoke testing.
- Do not assume a GPU is present. Run `scripts/check_env.py` first when the user asks for install/debug or runtime validation.
- Do not mix OpenAI `max_tokens` and native `max_new_tokens` unless translating between APIs.
- Grammar constraints are mutually exclusive in the native sampling params: choose one of `json_schema`, `regex`, or `ebnf`.
- Router/model gateway and disaggregation are deployment features; validate topology and ports before giving launch commands.
- Weight update and LoRA lifecycle endpoints are control-plane operations; use auth and versioning when exposed.
- Profiling, tracing, and request logging can change latency and may capture sensitive prompt data.
