# LoRA Workflows

## Server LoRA

Typical pattern:

```bash
vllm serve BASE_MODEL \
  --enable-lora \
  --lora-modules adapter_name=/path/or/model/id/to/adapter \
  --max-loras 4 \
  --max-lora-rank 64
```

Client requests use the served adapter name as `model`:

```json
{
  "model": "adapter_name",
  "messages": [{"role": "user", "content": "Say hello."}],
  "max_tokens": 16
}
```

## Runtime Updates

Runtime LoRA loading requires the server and environment to allow it. Set `VLLM_ALLOW_RUNTIME_LORA_UPDATING=true` only when the user accepts the security/operational implications. Then use the version-supported LoRA management routes to list/add/remove adapters.

## Offline LoRA

Offline LoRA uses `LoRARequest` in package APIs. Exact constructor signatures vary, so run:

```bash
python ../../scripts/inspect_api.py --object vllm.lora.request:LoRARequest
```

## Validation

- Base model must match adapter training base.
- Adapter rank must not exceed `--max-lora-rank`.
- Adapter names must be unique.
- Use stable `served-model-name` and adapter names in clients.
