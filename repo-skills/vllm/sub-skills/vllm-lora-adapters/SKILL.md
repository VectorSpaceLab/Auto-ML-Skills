---
name: vllm-lora-adapters
description: "Use when a user wants vLLM LoRA adapter serving or offline use, multi-LoRA configuration, runtime adapter add/remove/list, resolver plugins, or LoRA request payloads."
disable-model-invocation: true
---

# vLLM LoRA Adapters

Use this sub-skill for vLLM LoRA and adapter workflows after the root router selects it.

## Short Workflow

1. Confirm base model, adapter path/name, adapter rank, offline vs server mode, and whether runtime adapter updates are needed.
2. Read [references/workflows.md](references/workflows.md) for offline and serving flow.
3. Read [references/lora-reference.md](references/lora-reference.md) for flags, request model names, resolver plugin environment, and errors.
4. Validate adapter configuration before server launch; keep base model and adapter model names distinct in client requests.
5. For runtime adapter updates, explicitly set the required environment and smoke list/add/remove endpoints.

## Bundled Scripts

- [scripts/make_lora_payload.py](scripts/make_lora_payload.py): creates an OpenAI chat payload targeting a LoRA served model name.
- [scripts/validate_lora_config.py](scripts/validate_lora_config.py): validates LoRA server args and adapter naming.

## References

- [references/workflows.md](references/workflows.md): LoRA offline/server workflow.
- [references/lora-reference.md](references/lora-reference.md): LoRA flags, resolver plugins, runtime updates, and troubleshooting.

## Boundaries

This skill does not train LoRA adapters. Use it for vLLM loading, routing, and serving of already-created adapters.
