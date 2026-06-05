---
name: vllm-openai-serving
description: "Use when a user wants vLLM OpenAI-compatible server launch, health checks, models/chat/completions/responses/embeddings/score endpoint smoke tests, API keys, logs, or shutdown."
disable-model-invocation: true
---

# vLLM OpenAI Serving

Use this sub-skill after the root router selects `vllm-openai-serving`. It owns `vllm serve` lifecycle and OpenAI-compatible endpoint validation.

## Short Workflow

1. Confirm package/CLI with `../../scripts/check_env.py` and inspect endpoint classes with `../../scripts/inspect_api.py` if schemas are uncertain.
2. Resolve model ID, host, port, API key, config file, output directory, endpoint family, and whether to keep the server alive.
3. Read [references/workflows.md](references/workflows.md) for launch, wait, smoke, and shutdown sequence.
4. Read [references/endpoints.md](references/endpoints.md) for endpoint payloads and version-sensitive routes.
5. Start the server with a bounded lifecycle helper; record PID and logs.
6. Smoke `/health`, `/v1/models`, and the requested endpoint; then shut down unless the user explicitly requested a persistent server.

## Bundled Scripts

- [scripts/start_server.py](scripts/start_server.py): start/wait/smoke/manage `vllm serve` with PID/log files.
- [scripts/client_smoke.py](scripts/client_smoke.py): wrapper around root OpenAI client smoke helper.

## References

- [references/workflows.md](references/workflows.md): safe server lifecycle and command patterns.
- [references/endpoints.md](references/endpoints.md): request bodies for chat, completions, responses, embeddings, score, health, metrics, and models.

## Boundaries

For choosing engine args or YAML, use `vllm-serving-config`. For LoRA server behavior, route to `vllm-lora-adapters` after the base server plan is clear.
