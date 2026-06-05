---
name: vllm-offline-inference
description: "Use when a user wants vLLM offline LLM inference, SamplingParams, chat templates, batch generation, CLI chat/complete/run-batch, or a local model-loading smoke test."
disable-model-invocation: true
---

# vLLM Offline Inference

Use this sub-skill after the root `vllm` router selects `vllm-offline-inference`. It covers package API inference with `LLM`, `SamplingParams`, `llm.generate`, `llm.chat`, CLI chat/complete/batch commands, and local batch request preparation.

## Use When

- The user wants Python-side `LLM.generate`, `LLM.chat`, `SamplingParams`, or a minimal model-load smoke test.
- The user wants `vllm chat`, `vllm complete`, or `vllm run-batch` without running a persistent server.
- The user asks how to prepare prompts, chat messages, sampling settings, or JSONL batch requests.
- The user needs a bounded real smoke with a small model before attempting larger workflows.

## Inputs To Collect

- Model ID or user-provided local model path, dtype, max model length, GPU memory utilization, eager/compile preferences, prompts, and output token limit.
- Whether chat template behavior matters, whether batch JSONL is required, and where to save outputs.
- Whether the validation should be dry-run only or can load a model.

## Short Workflow

1. Confirm the environment with `../../scripts/check_env.py`; use `--deep-import` only when package imports are in question.
2. Resolve model ID, cache policy, output directory, prompt set, chat-vs-completion mode, and whether an actual model load is allowed.
3. Read [references/workflows.md](references/workflows.md) for API patterns and smoke/full-run decisions.
4. Read [references/cli-reference.md](references/cli-reference.md) when using `vllm chat`, `vllm complete`, or `vllm run-batch`.
5. Use the bundled scripts below for dry-run payloads or bounded smoke tests.
6. Save prompts, sampling params, generated text, token counts if available, stdout/stderr, and a summary JSON.
7. Shut down/release the engine after the smoke and confirm no managed process remains.

## Bundled Scripts

- [scripts/run_offline_smoke.py](scripts/run_offline_smoke.py): dry-run or real `LLM.generate`/`LLM.chat` smoke; run `python scripts/run_offline_smoke.py --help` first.
- [scripts/make_batch_requests.py](scripts/make_batch_requests.py): create JSONL batch requests for `vllm run-batch`.

## References

- [references/workflows.md](references/workflows.md): offline API usage, SamplingParams, chat templates, and output inspection.
- [references/cli-reference.md](references/cli-reference.md): CLI batch/chat/complete command patterns and request JSONL schemas.

## Boundaries

For server endpoints, return to `vllm-openai-serving`. For pooling/reranking, use `vllm-embeddings-pooling`. For structured output constraints, use `vllm-structured-outputs`.

## Verification Notes

- `--help` and `--dry-run` do not prove model execution.
- A real smoke must import vLLM, load the model, generate text, write a report, and release resources.
- Use a public model ID in reusable examples; task-specific local model paths belong only in the user's command, not in this skill.
