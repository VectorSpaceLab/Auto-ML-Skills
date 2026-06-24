---
name: vllm-lora-adapters
description: "Use when a user wants vLLM LoRA adapter serving or offline use, multi-LoRA configuration, runtime adapter add/remove/list, resolver plugins, or LoRA request payloads."
disable-model-invocation: true
---

# vLLM LoRA Adapters

Use this sub-skill for vLLM LoRA and adapter workflows after the root router selects it. It handles loading, serving, routing, and validating already-created adapters; it does not train LoRA adapters.

## Use When

- The user wants offline or server-side LoRA adapter use with vLLM.
- The user needs multi-LoRA setup, runtime add/remove/list endpoints, adapter resolver plugins, or request payloads that target adapter model names.
- The user has a base model plus adapter artifact and wants to verify compatibility.
- The user asks why the server serves only the base model or why adapter names are not listed.

## Inputs To Collect

- Base model ID, adapter path or public ID, adapter served name, rank/capacity limits, tokenizer compatibility, and expected target modules.
- Offline versus server workflow, runtime-update needs, resolver plugin environment, auth, and output/log location.
- Exact client model field expected for base and adapter requests.

## Short Workflow

1. Confirm base model, adapter path/name, adapter rank, offline vs server mode, and whether runtime adapter updates are needed.
2. Read [references/workflows.md](references/workflows.md) for offline and serving flow.
3. Read [references/lora-reference.md](references/lora-reference.md) for flags, request model names, resolver plugin environment, and errors.
4. Validate adapter configuration before server launch; keep base model and adapter model names distinct in client requests.
5. For runtime adapter updates, explicitly set the required environment and smoke list/add/remove endpoints.
6. Smoke base and adapter requests separately before reporting success.

## Bundled Scripts

- [scripts/make_lora_payload.py](scripts/make_lora_payload.py): creates an OpenAI chat payload targeting a LoRA served model name.
- [scripts/validate_lora_config.py](scripts/validate_lora_config.py): validates LoRA server args and adapter naming.

## References

- [references/workflows.md](references/workflows.md): LoRA offline/server workflow.
- [references/lora-reference.md](references/lora-reference.md): LoRA flags, resolver plugins, runtime updates, and troubleshooting.

## Boundaries

This skill does not train LoRA adapters. Use it for vLLM loading, routing, and serving of already-created adapters.

## Verification Notes

- Config and payload validators do not prove the adapter generates correctly.
- Real LoRA validation requires loading a compatible adapter and confirming the adapter model name is accepted by the target API.
- If no adapter artifact is available, report static validation only.
