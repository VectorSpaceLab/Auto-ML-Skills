# OpenAI-Compatible Server Reference

## Entrypoints

Preferred launch forms:

```bash
python -m sglang.launch_server --model-path <MODEL_ID> --host 127.0.0.1 --port 30000
sglang serve --model-path <MODEL_ID> --host 127.0.0.1 --port 30000
```

Common server args:

- Model/tokenizer: `--model-path`, `--tokenizer-path`, `--trust-remote-code`, `--dtype`, `--kv-cache-dtype`, `--quantization`, `--context-length`.
- HTTP: `--host`, `--port`, `--api-key`, `--admin-api-key`, `--served-model-name`, TLS flags, `--enable-http2`.
- Runtime: `--tp-size`/`--tp`, `--dp-size`, `--pp-size`, `--mem-fraction-static`, `--max-running-requests`, `--max-total-tokens`, `--chunked-prefill-size`.
- API: `--chat-template`, `--hf-chat-template-name`, `--reasoning-parser`, `--tool-call-parser`, `--sampling-defaults`.
- Observability: `--log-requests`, `--enable-metrics`, `--enable-trace`, `--otlp-traces-endpoint`.

## Routes

Inspected routes include:

- Health/info: `/health`, `/health_generate`, `/get_model_info`, `/model_info`, `/get_server_info`, `/server_info`, `/get_load`, `/v1/loads`, `/v1/models`, `/v1/models/{model}`.
- Native inference: `/generate`, `/encode`, `/classify`, `/flush_cache`, `/abort_request`, `/open_session`, `/close_session`.
- OpenAI-compatible: `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/classify`, `/v1/score`, `/v1/rerank`, `/v1/responses`, `/v1/tokenize`, `/v1/detokenize`, `/v1/audio/transcriptions`, `/v1/realtime`.
- Compatibility: Ollama `/api/chat`, `/api/generate`, `/api/tags`, `/api/show`; Anthropic `/v1/messages`; SageMaker `/ping`, `/invocations`; Vertex `AIP_PREDICT_ROUTE` default `/vertex_generate`.
- Admin/control: profile, trace level, logging, LoRA load/unload, weight update, HiCache storage backend.

## OpenAI Client Smoke

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:30000/v1", api_key="None")
print(client.models.list())
resp = client.chat.completions.create(
    model="<MODEL_ID>",
    messages=[{"role": "user", "content": "Reply with one word."}],
    max_tokens=8,
    temperature=0,
)
print(resp.choices[0].message.content)
```

Use native `/generate` when the user needs `max_new_tokens`, `lora_path`, native logprob controls, or non-OpenAI features. Use `/v1/chat/completions` when client compatibility and chat templates matter.

## Lifecycle Safety

- Bind to `127.0.0.1` for local testing. Use auth and TLS/reverse proxy before exposing externally.
- Check `/health` first; it may include warmup behavior depending on server state.
- Avoid `killall_sglang` in shared environments unless the user explicitly asks.
- Use unique ports for multiple servers and record PIDs.
