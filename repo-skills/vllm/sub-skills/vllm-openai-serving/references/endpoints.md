# Endpoint Reference

## Health And Discovery

- `GET /health`: readiness probe.
- `GET /metrics`: Prometheus metrics when exposed.
- `GET /v1/models`: list served model aliases.
- `GET /version`: package/server version when exposed.
- `GET /load`: server load metrics when exposed.
- `POST /tokenize` and `POST /detokenize`: utility routes in supported server builds.

## Chat Completions

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "messages": [{"role": "user", "content": "Say hello."}],
  "temperature": 0,
  "max_tokens": 16
}
```

## Completions

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "prompt": "The fastest way to test vLLM is",
  "temperature": 0,
  "max_tokens": 16
}
```

## Responses

The Responses API is present in current vLLM entrypoints for text-generation models:

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "input": "Say hello in one short sentence.",
  "temperature": 0,
  "max_output_tokens": 16
}
```

Responses tool calling uses the Responses request schema, not the chat-completions schema. Validate with `../../scripts/inspect_api.py`, then smoke `/v1/responses` independently from `/v1/chat/completions`.

## Embeddings

Use an embedding/pooling model:

```json
{
  "model": "BAAI/bge-small-en-v1.5",
  "input": ["hello", "world"]
}
```

## Score/Rerank

Score endpoints are runner- and version-sensitive. Public endpoint families include:

- `/score` or `/v1/score` for score models.
- `/rerank`, `/v1/rerank`, or `/v2/rerank` for Cohere/Jina-style rerank.
- `/pooling` for generic pooling models.
- `/classify` for classification models.
- `/generative_scoring` for CausalLM next-token label scoring.

Inspect installed request classes and use `vllm-embeddings-pooling` scripts to generate candidate payloads.

## Speech And Realtime

Speech routes require ASR-capable models and audio extras:

- `/v1/audio/transcriptions`
- `/v1/audio/translations`
- WebSocket `/v1/realtime` for streaming transcription

Realtime clients send base64 PCM16 audio chunks at 16 kHz mono with `input_audio_buffer.append` and `input_audio_buffer.commit` events. Do not use a normal text-generation model for these routes.

## Model Aliases, Tokenizer, And Chat Template

Use `--served-model-name` when clients need a stable model alias distinct from the model ID/path. `/v1/models` should show the alias, and request `model` must match it.

Chat endpoints require a tokenizer chat template. If the tokenizer lacks one, provide `--chat-template` and, when needed, `--chat-template-content-format string|openai`. Use `--tokenizer` only when the tokenizer should differ from the model.

## Authorization

When `--api-key` or `VLLM_API_KEY` is configured, send:

```text
Authorization: Bearer <key>
```

## Failure Interpretation

- 404: route unsupported by this version or wrong endpoint family.
- 422: payload schema mismatch.
- 400: model/runner/guided decoding/tool parameter rejected.
- 500: model execution or server-side failure; inspect server log.
