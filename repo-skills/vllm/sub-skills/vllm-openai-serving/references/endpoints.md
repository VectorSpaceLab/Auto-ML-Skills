# Endpoint Reference

## Health And Discovery

- `GET /health`: readiness probe.
- `GET /metrics`: Prometheus metrics when exposed.
- `GET /v1/models`: list served model aliases.

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

The Responses API is present in current vLLM entrypoints. Validate schema with `../../scripts/inspect_api.py`; request support depends on installed version.

## Embeddings

Use an embedding/pooling model:

```json
{
  "model": "BAAI/bge-small-en-v1.5",
  "input": ["hello", "world"]
}
```

## Score/Rerank

Score endpoints are version-sensitive. Inspect installed request classes and use `vllm-embeddings-pooling` scripts to generate candidate payloads.

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
