---
name: sglang-lora-weight-updates
description: "Use SGLang LoRA adapter serving, multi-LoRA batching, adapter lifecycle APIs, and runtime weight update endpoints."
disable-model-invocation: true
---

# SGLang LoRA And Weight Updates

Use this sub-skill for `--enable-lora`, adapter paths, `/load_lora_adapter`, `/unload_lora_adapter`, native `lora_path`, multi-LoRA batching, and weight-update endpoints for RL/post-training. It assumes the user already has compatible adapter or weight artifacts; it does not train adapters.

Read [references/lora-weight-updates.md](references/lora-weight-updates.md) for lifecycle APIs, payload shapes, weight update controls, and safety notes. Use [scripts/validate_lora_payload.py](scripts/validate_lora_payload.py) to lint adapter lifecycle payloads before calling admin endpoints.

## Use When

- The user wants to serve one or more LoRA adapters on a base model.
- The user needs runtime load/unload/list behavior, named adapters, or per-request `lora_path`.
- The user is wiring RL/post-training weight synchronization into a running SGLang server.
- The user needs to verify adapter/base model compatibility before starting traffic.

## Inputs To Collect

- Base model ID, adapter names, adapter paths or public IDs, ranks, target modules, tokenizer compatibility, and desired served model names.
- Server auth/admin auth, allowed adapter storage locations, concurrency limits, and whether runtime updates are enabled.
- For weight updates: distributed group shape, update source, versioning, rollback path, and isolation requirements.

## Workflow

1. Confirm the base model and adapter compatibility.
2. Launch with LoRA enabled and capacity limits sized for expected concurrency.
3. Prefer named adapter lifecycle APIs for serving; use per-request `lora_path` only for controlled native calls.
4. For weight sync/update workflows, validate admin auth and distributed group lifecycle before sending tensors or disk paths.
5. Smoke base model and adapter model names separately before exposing the service.

## Verification

- Run the validator on load/unload payloads before sending them to a live server.
- Validate `/v1/models` or adapter list behavior after each load/unload.
- Do not claim real LoRA correctness unless a compatible adapter was actually loaded and generated from.

## Boundaries

Use `sglang-openai-server` for server startup/shutdown and client requests. Use `sglang-distributed-topology` for distributed weight sync. Use `sglang-cache-performance` only after adapter routing is correct.
