---
name: sglang-openai-server
description: "Launch, validate, and use SGLang OpenAI-compatible and native HTTP servers safely."
disable-model-invocation: true
---

# SGLang OpenAI Server

Use this sub-skill for server startup/shutdown, health checks, `/v1` clients, native HTTP endpoints, auth, streaming, and lifecycle testing. It owns the safe local loop of start, wait, smoke, and stop for SGLang HTTP servers.

Read [references/openai-server.md](references/openai-server.md) for launch commands, route families, OpenAI client examples, Responses API notes, and lifecycle safety. Use [scripts/server_helper.py](scripts/server_helper.py) to start/stop/status a managed local server, and [scripts/openai_client_smoke.py](scripts/openai_client_smoke.py) to validate `/health`, `/v1/models`, and optional chat/completions. Both scripts support `--help` without loading a model.

## Use When

- The user wants `python -m sglang.launch_server`, `sglang serve`, OpenAI-compatible clients, native HTTP requests, or server health checks.
- The user needs `/v1/chat/completions`, `/v1/completions`, `/v1/responses`, `/v1/models`, `/generate`, `/health`, streaming, or API-key behavior.
- The user asks for a reproducible local smoke test with a small model.
- The user wants to keep or stop a managed server process.

## Inputs To Collect

- Model ID or user-provided model path, served model name, host, port, API/admin keys, context length, dtype, memory fraction, and output directory for logs/PID.
- Endpoint family, request payload, streaming needs, and whether the server must remain running.
- Any cross-cutting features: tools/reasoning parser, structured output, multimodal, LoRA, distributed topology, or metrics.

## Workflow

1. Choose model and port. Use `Qwen/Qwen3-0.6B` only when the environment can run it; otherwise keep `<MODEL_ID>`.
2. Start with `python -m sglang.launch_server --model-path <MODEL_ID> --host 127.0.0.1 --port 30000`.
3. Poll `/health` before sending OpenAI client requests.
4. Validate `/v1/models`, then the specific route the user needs.
5. Stop the server when the task is complete unless the user requested a persistent process.
6. Save client responses and server logs for debugging when a smoke fails.

## Verification

- Use the helper script for managed local starts; it writes PID/logs and can stop by PID file.
- Use the client smoke script for `/health`, `/v1/models`, and one short chat/completion request.
- A passing health check is not enough for endpoint correctness; smoke the exact route the user will call.

## Boundaries

Use `sglang-offline-runtime` when no HTTP server is needed. Use `sglang-tool-reasoning`, `sglang-structured-outputs`, `sglang-multimodal-serving`, or `sglang-lora-weight-updates` when endpoint payloads require those feature-specific details. Use `sglang-install-build-troubleshooting` when the server fails before health.
