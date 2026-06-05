---
name: vllm-offline-inference
description: "Use when a user wants vLLM offline LLM inference, SamplingParams, chat templates, batch generation, CLI chat/complete/run-batch, or a local model-loading smoke test."
disable-model-invocation: true
---

# vLLM Offline Inference

Use this sub-skill after the root `vllm` router selects `vllm-offline-inference`. It covers package API inference with `LLM`, `SamplingParams`, `llm.generate`, `llm.chat`, and local batch request preparation.

## Short Workflow

1. Confirm the environment with `../../scripts/check_env.py`; use `--deep-import` only when package imports are in question.
2. Resolve model ID, cache policy, output directory, prompt set, chat-vs-completion mode, and whether an actual model load is allowed.
3. Read [references/workflows.md](references/workflows.md) for API patterns and smoke/full-run decisions.
4. Read [references/cli-reference.md](references/cli-reference.md) when using `vllm chat`, `vllm complete`, or `vllm run-batch`.
5. Use the bundled scripts below for dry-run payloads or bounded smoke tests.
6. Save prompts, sampling params, generated text, token counts if available, stdout/stderr, and a summary JSON.

## Bundled Scripts

- [scripts/run_offline_smoke.py](scripts/run_offline_smoke.py): dry-run or real `LLM.generate`/`LLM.chat` smoke; run `python scripts/run_offline_smoke.py --help` first.
- [scripts/make_batch_requests.py](scripts/make_batch_requests.py): create JSONL batch requests for `vllm run-batch`.

## References

- [references/workflows.md](references/workflows.md): offline API usage, SamplingParams, chat templates, and output inspection.
- [references/cli-reference.md](references/cli-reference.md): CLI batch/chat/complete command patterns and request JSONL schemas.

## Boundaries

For server endpoints, return to `vllm-openai-serving`. For pooling/reranking, use `vllm-embeddings-pooling`. For structured output constraints, use `vllm-structured-outputs`.
