---
name: sglang-openai-server
description: "Launch, validate, and use SGLang OpenAI-compatible and native HTTP servers safely."
disable-model-invocation: true
---

# SGLang OpenAI Server

Use this sub-skill for server startup/shutdown, health checks, `/v1` clients, native HTTP endpoints, auth, streaming, and lifecycle testing.

Read [references/openai-server.md](references/openai-server.md). Use [scripts/server_helper.py](scripts/server_helper.py) to start/stop/status a managed local server, and [scripts/openai_client_smoke.py](scripts/openai_client_smoke.py) to validate `/health`, `/v1/models`, and optional chat/completions. Both scripts support `--help` without loading a model.

## Workflow

1. Choose model and port. Use `Qwen/Qwen3-0.6B` only when the environment can run it; otherwise keep `<MODEL_ID>`.
2. Start with `python -m sglang.launch_server --model-path <MODEL_ID> --host 127.0.0.1 --port 30000`.
3. Poll `/health` before sending OpenAI client requests.
4. Validate `/v1/models`, then the specific route the user needs.
5. Stop the server when the task is complete unless the user requested a persistent process.
