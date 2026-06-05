---
name: sglang-offline-runtime
description: "Use SGLang offline Runtime, Engine, language frontend, native generation API, sampling parameters, and chat-template workflows."
disable-model-invocation: true
---

# SGLang Offline Runtime

Use this sub-skill for Python-side inference, native `/generate` payloads, language frontend programs, sampling parameters, chat templates, and offline Engine workflows.

Read [references/offline-runtime.md](references/offline-runtime.md) for API patterns, sampling params, native request shapes, and common pitfalls. Use [scripts/run_offline_smoke.py](scripts/run_offline_smoke.py) to run a small offline smoke when the user provides a runnable model/environment; `--help` is safe.

## Workflow

1. Decide whether the user needs offline Python (`Runtime`/Engine), language frontend decorators, or native HTTP `/generate`.
2. For public docs use `<MODEL_ID>` or `Qwen/Qwen3-0.6B`; do not embed local model paths.
3. Keep native sampling params as SGLang names such as `max_new_tokens`; translate to OpenAI names only when crossing to `/v1`.
4. For constrained generation through the frontend, pass `regex`, `json_schema`, `dtype`, or `choices` through `sgl.gen`/`sgl.select`.
5. For multimodal offline requests, route to `sglang-multimodal-serving` as well.
