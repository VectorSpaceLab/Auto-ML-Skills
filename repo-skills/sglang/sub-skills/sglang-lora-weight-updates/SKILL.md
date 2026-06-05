---
name: sglang-lora-weight-updates
description: "Use SGLang LoRA adapter serving, multi-LoRA batching, adapter lifecycle APIs, and runtime weight update endpoints."
disable-model-invocation: true
---

# SGLang LoRA And Weight Updates

Use this sub-skill for `--enable-lora`, adapter paths, `/load_lora_adapter`, `/unload_lora_adapter`, native `lora_path`, multi-LoRA batching, and weight-update endpoints for RL/post-training.

Read [references/lora-weight-updates.md](references/lora-weight-updates.md). Use [scripts/validate_lora_payload.py](scripts/validate_lora_payload.py) to lint adapter lifecycle payloads.

## Workflow

1. Confirm the base model and adapter compatibility.
2. Launch with LoRA enabled and capacity limits sized for expected concurrency.
3. Prefer named adapter lifecycle APIs for serving; use per-request `lora_path` only for controlled native calls.
4. For weight sync/update workflows, validate admin auth and distributed group lifecycle before sending tensors or disk paths.
