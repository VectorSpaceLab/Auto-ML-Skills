---
name: sglang-offline-runtime
description: "Use SGLang offline Runtime, Engine, language frontend, native generation API, sampling parameters, and chat-template workflows."
disable-model-invocation: true
---

# SGLang Offline Runtime

Use this sub-skill for Python-side inference, native `/generate` payloads, language frontend programs, sampling parameters, chat templates, and offline Engine workflows. It is the first choice when the user wants model execution without managing an HTTP server.

Read [references/offline-runtime.md](references/offline-runtime.md) for API patterns, sampling params, native request shapes, and common pitfalls. Use [scripts/run_offline_smoke.py](scripts/run_offline_smoke.py) to run a small offline smoke when the user provides a runnable model/environment; `--help` and `--dry-run` are safe, and reports should use `--report-model-name` for local paths.

## Use When

- The user wants `sgl.Engine`, `Runtime`, `RuntimeEndpoint`, `@sgl.function`, `sgl.gen`, `sgl.select`, or role helpers.
- The user wants native `/generate` payloads but does not need OpenAI-compatible chat clients.
- The user needs a one-prompt model-load smoke test with bounded context length and token count.
- The user asks how native sampling names differ from OpenAI-compatible request names.

## Inputs To Collect

- Model ID or user-provided local model path, available GPU/accelerator, dtype, context length, memory fraction, prompts, and output limit.
- Offline API style: direct `Engine.generate`, frontend function, remote `RuntimeEndpoint`, or native HTTP payload.
- Whether constrained generation, multimodal fields, LoRA, logprobs, or hidden states are required.

## Workflow

1. Decide whether the user needs offline Python (`Runtime`/Engine), language frontend decorators, or native HTTP `/generate`.
2. For public docs use `<MODEL_ID>` or `Qwen/Qwen3-0.6B`; do not embed local model paths.
3. Keep native sampling params as SGLang names such as `max_new_tokens`; translate to OpenAI names only when crossing to `/v1`.
4. For constrained generation through the frontend, pass `regex`, `json_schema`, `dtype`, or `choices` through `sgl.gen`/`sgl.select`.
5. For multimodal offline requests, route to `sglang-multimodal-serving` as well.
6. Always shut down `Engine` instances in a `finally` block or through the smoke script helper.

## Verification

- Start with `python scripts/run_offline_smoke.py --help`; then use `--dry-run` if the model path or hardware is uncertain.
- For a real smoke, use a small prompt, `max_new_tokens` near 4, reduced context length, and a safe report model name.
- Record whether the smoke actually loaded the model and generated output; do not count import-only checks as runtime validation.

## Boundaries

Use `sglang-openai-server` for `/v1/chat/completions`, `/v1/responses`, auth, or persistent service processes. Use `sglang-structured-outputs` for grammar/schema design. Use `sglang-cache-performance` only after a minimal offline generation succeeds.
