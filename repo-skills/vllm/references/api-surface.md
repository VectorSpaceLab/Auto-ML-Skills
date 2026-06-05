# vLLM API Surface Reference

## Verified Public Surfaces

The public package exposes:

- Console script: `vllm = vllm.entrypoints.cli.main:main`.
- Offline APIs: `from vllm import LLM, SamplingParams`.
- Offline generation: `llm.generate(prompts, sampling_params)`.
- Offline chat: `llm.chat(messages_list, sampling_params)`.
- Pooling/embedding: `llm.encode(...)` for pooling runners.
- Reranking/scoring: `llm.score(text_1, text_2, ...)` when the selected model and runner support scoring.
- OpenAI-compatible server: `vllm serve MODEL [args]`.
- Benchmark CLI: `vllm bench latency|throughput|serve|startup|mm-processor|sweep`.

Use `scripts/inspect_api.py` in the installed environment to re-check signatures and endpoint request classes for the user's version.

## CLI Families

- `vllm serve`: starts a model server. Accepts model ID/path plus engine/server args and optional `--config`.
- `vllm chat`: command-line interactive chat through vLLM.
- `vllm complete`: command-line prompt completion.
- `vllm run-batch`: batch OpenAI-format requests against local engine/server code.
- `vllm bench`: latency, throughput, serve, startup, mm-processor, and sweep benchmarks.
- `vllm collect-env`: environment diagnostics.

## OpenAI-Compatible Endpoint Families

Common routes in current vLLM serving:

- `GET /health`
- `GET /metrics`
- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/completions`
- `POST /v1/responses`
- `POST /v1/embeddings`
- `POST /score` or `/v1/score` depending on package version and serving configuration
- Tokenization/rendering routes when enabled by the server build
- LoRA management routes when runtime LoRA updating is enabled

Always validate with `openai_client_smoke.py --base-url ... --list-models` or direct `curl` before relying on a route.

## Request Patterns

Generation:

```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen3-0.6B", generation_config="vllm")
params = SamplingParams(temperature=0.0, max_tokens=32)
outputs = llm.generate(["Write one sentence about vLLM."], params)
print(outputs[0].outputs[0].text)
```

Chat:

```python
messages = [[{"role": "user", "content": "Answer in one short sentence."}]]
outputs = llm.chat(messages, params)
```

OpenAI chat request:

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "messages": [{"role": "user", "content": "Say hello."}],
  "temperature": 0,
  "max_tokens": 16
}
```

Structured JSON request:

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "messages": [{"role": "user", "content": "Return a city and country."}],
  "guided_json": {
    "type": "object",
    "properties": {
      "city": {"type": "string"},
      "country": {"type": "string"}
    },
    "required": ["city", "country"]
  },
  "max_tokens": 64
}
```

Embedding request:

```json
{
  "model": "BAAI/bge-small-en-v1.5",
  "input": ["hello", "world"]
}
```

Score request shape varies by version; inspect request schemas and smoke with a small cross-encoder/reranker model before production use.
