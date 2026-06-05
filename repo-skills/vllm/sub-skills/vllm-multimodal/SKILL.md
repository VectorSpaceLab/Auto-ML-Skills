---
name: vllm-multimodal
description: "Use when a user wants vLLM multimodal image, video, audio, prompt embedding, processor kwargs, vision-language chat payloads, or speech transcription/translation endpoint workflows."
disable-model-invocation: true
---

# vLLM Multimodal

Use this sub-skill for vLLM multimodal models and media-bearing requests. It owns image, video, audio, prompt embedding, processor kwargs, vision-language chat payloads, and speech transcription/translation endpoint workflows.

## Use When

- The user wants image, video, audio, prompt embeddings, or speech endpoints through vLLM.
- The user needs OpenAI-style content blocks, base64 media, URLs, local media paths, or processor kwargs.
- The user asks whether a model and prompt template are valid for multimodal serving.
- The user needs to separate text-only server validation from true multimodal validation.

## Inputs To Collect

- Model ID, modality, prompt template/placeholders, processor options, media source, media size, endpoint family, and privacy limits.
- Whether the server can fetch URLs or needs base64/local file access.
- Output length, sampling settings, and whether transcription/translation or chat generation is expected.

## Short Workflow

1. Identify modality: image, video, audio, prompt embeddings, or speech endpoint.
2. Confirm the chosen model is supported by vLLM for that modality and that the prompt template includes required placeholders.
3. Read [references/workflows.md](references/workflows.md) for offline/server flow.
4. Read [references/multimodal-reference.md](references/multimodal-reference.md) for payload shapes, media URLs/base64, and processor kwargs.
5. Validate media references before model loading; use small media and short outputs for smoke tests.
6. Record whether the real smoke used text-only, image, video, audio, or speech input.

## Bundled Scripts

- [scripts/make_mm_payload.py](scripts/make_mm_payload.py): creates image/audio/video chat request payloads.
- [scripts/validate_media_payload.py](scripts/validate_media_payload.py): checks payload structure and local media paths/URLs.

## References

- [references/workflows.md](references/workflows.md): multimodal workflow.
- [references/multimodal-reference.md](references/multimodal-reference.md): media payload, placeholders, and troubleshooting.

## Boundaries

Use `vllm-openai-serving` for server lifecycle and `vllm-performance-tuning` for multimodal compile/cache tuning.

## Verification Notes

- Payload validation is structural only.
- A Qwen text-only model can validate vLLM server lifecycle, but not multimodal payload semantics.
- True multimodal validation requires a compatible VLM/audio/speech model and an actual small media sample.
