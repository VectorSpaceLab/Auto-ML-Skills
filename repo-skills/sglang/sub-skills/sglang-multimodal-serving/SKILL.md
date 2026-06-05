---
name: sglang-multimodal-serving
description: "Use SGLang vision-language, image/audio/video, multimodal embedding, ASR, and diffusion generation serving workflows."
disable-model-invocation: true
---

# SGLang Multimodal Serving

Use this sub-skill for VLM OpenAI payloads, native `image_data`/`audio_data`/`video_data`, multimodal embeddings, ASR/realtime audio routes, and diffusion `sglang generate/serve` workflows. It owns payload shape and model-modality checks, not ordinary text-only chat.

Read [references/multimodal-serving.md](references/multimodal-serving.md) for vision/audio/video payload examples, native fields, and diffusion environment notes. Use [scripts/validate_multimodal_payload.py](scripts/validate_multimodal_payload.py) to lint OpenAI-style multimodal message content before sending it.

## Use When

- The user wants image, video, or audio input with chat/completions or native `/generate`.
- The user wants multimodal embeddings, ASR transcription, realtime audio, or diffusion generation.
- The user asks how to represent media as URL, base64, file path, or native fields.
- The user needs to separate text-only Qwen-style smoke tests from real multimodal validation.

## Inputs To Collect

- Model ID, modality support, processor requirements, chat template, media source, media size, and privacy constraints.
- Endpoint family: OpenAI chat, native `/generate`, embeddings, audio transcription, realtime, or diffusion CLI/server.
- Whether the server can fetch remote URLs or needs local/base64 payloads.

## Workflow

1. Confirm model modality: text-only, VLM, ASR/audio, embedding, or diffusion/image/video generation.
2. Use an explicit multimodal model placeholder such as `<VLM_MODEL_ID>` unless the user provides a public model ID.
3. For OpenAI vision, send content blocks with `type: text` and `type: image_url`.
4. For native SGLang, use `/generate` with `image_data` or `audio_data`.
5. For diffusion, use `sglang serve/generate --model-type diffusion` or let CLI auto-detect when the installed build supports diffusion extras.
6. Keep media samples tiny for smoke tests and record whether the request used URL, base64, or local file access.

## Verification

- Run the payload validator before model loading.
- Validate with a true multimodal model for modality correctness; a text-only Qwen model can only verify the server lifecycle, not multimodal semantics.
- For remote URLs, confirm the server process has network access and does not leak private media.

## Boundaries

Use `sglang-openai-server` for generic server lifecycle. Use `sglang-embeddings-rerank-score` for embedding/rerank output interpretation. Use `sglang-install-build-troubleshooting` when modality extras or diffusion dependencies fail to import.
