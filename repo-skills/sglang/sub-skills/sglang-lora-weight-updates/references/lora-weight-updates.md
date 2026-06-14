# LoRA And Weight Update Reference

## Server Args

LoRA-related ServerArgs include:

- `--enable-lora`.
- `--max-lora-rank`.
- `--lora-target-modules`.
- `--lora-paths`.
- `--max-loaded-loras`.
- `--max-loras-per-batch`.
- `--lora-eviction-policy`.
- `--lora-backend`.
- `--max-lora-chunk-size`.
- `--enable-lora-overlap-loading`.
- `--lora-strict-loading`.

Launch pattern:

```bash
python -m sglang.launch_server \
  --model-path <BASE_MODEL_ID> \
  --enable-lora \
  --max-loaded-loras 4 \
  --max-loras-per-batch 4 \
  --host 127.0.0.1 --port 30000
```

## Adapter Lifecycle Routes

Inspected routes:

- `POST /load_lora_adapter`
- `POST /load_lora_adapter_from_tensors`
- `POST /unload_lora_adapter`

Generic load payload:

```json
{
  "lora_name": "adapter-a",
  "lora_path": "<LORA_ADAPTER_PATH_OR_ID>"
}
```

Generic unload payload:

```json
{
  "lora_name": "adapter-a"
}
```

## Per-Request Native LoRA

Native `/generate` supports `lora_path` in the request. This is useful for controlled experiments, but production serving should prefer preloaded/named adapters to avoid unpredictable load latency.

## Weight Update Routes

Inspected routes include:

- `POST /update_weights_from_disk`
- `POST /init_weights_update_group`
- `POST /destroy_weights_update_group`
- `POST /update_weights_from_tensor`
- `POST /update_weights_from_distributed`
- `POST /update_weights_from_ipc`
- `POST /update_weight_version`
- Remote instance transfer routes for sending weights between instances.

These are operationally sensitive. Use admin auth when exposed, check versioning, and validate distributed group init/destroy around tensor updates.

## Pitfalls

- Adapter rank or target modules incompatible with base model.
- Loading too many adapters causes memory pressure; set max-loaded and eviction policy deliberately.
- Hot-loading adapters during traffic can add latency unless overlap loading is enabled and tested.
- Weight updates can desynchronize replicas if routed traffic continues during update; drain or version traffic.
