# Model Selection Reference

## Smoke Model Rules

For public-ready examples, prefer public model IDs. Do not write local model paths into generated skill docs, commands, or examples.

Recommended text-generation smoke model:

- `Qwen/Qwen3-0.6B` when accessible.

Fallbacks when the preferred model is unavailable:

- A caller-provided public model ID.
- A smaller public causal LM supported by the installed vLLM version, such as `facebook/opt-125m`, when the task is only API plumbing.
- A production model specified by the user.

## Choosing A Runner

- Text generation/chat: causal or instruct/chat model; use `LLM(..., generation_config="vllm")` for deterministic smoke defaults.
- Embeddings: embedding/pooling model, often served with `--runner pooling` or model auto-detection.
- Reranker/score: cross-encoder or reward/rerank model that supports scoring.
- Multimodal: vision-language/audio model with vLLM support and correct prompt placeholders.
- Speech: transcription/translation models through speech endpoints.

## Sizing Heuristics

- Fit model weights plus KV cache into available GPU memory. Lower `--gpu-memory-utilization`, `--max-model-len`, and concurrency if OOM occurs.
- Use `--dtype auto` first. Force `float16`/`bfloat16` only when model and hardware support it.
- Use `--tensor-parallel-size N` when a single model copy must span N GPUs.
- Use data parallel or multiple server replicas when the model fits per replica and request throughput is the bottleneck.
- Use quantized model IDs or `--quantization` only when the model and selected backend support the method.

## Access And Download

- Confirm model license and gated access before starting long runs.
- Set cache directories deliberately in shared environments.
- For smoke tests, use `--max-model-len` and `max_tokens` small enough to keep startup and generation bounded.
