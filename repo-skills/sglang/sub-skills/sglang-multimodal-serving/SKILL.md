---
name: sglang-multimodal-serving
description: "Use SGLang vision-language, image/audio/video, multimodal embedding, ASR, and diffusion generation serving workflows."
disable-model-invocation: true
---

# SGLang Multimodal Serving

Use this sub-skill for VLM OpenAI payloads, native `image_data`/`audio_data`, multimodal embeddings, ASR routes, and diffusion `sglang generate/serve` workflows.

Read [references/multimodal-serving.md](references/multimodal-serving.md). Use [scripts/validate_multimodal_payload.py](scripts/validate_multimodal_payload.py) to lint OpenAI-style multimodal message content.

## Workflow

1. Confirm model modality: text-only, VLM, ASR/audio, embedding, or diffusion/image/video generation.
2. Use an explicit multimodal model placeholder such as `<VLM_MODEL_ID>` unless the user provides a public model ID.
3. For OpenAI vision, send content blocks with `type: text` and `type: image_url`.
4. For native SGLang, use `/generate` with `image_data` or `audio_data`.
5. For diffusion, use `sglang serve/generate --model-type diffusion` or let CLI auto-detect when the installed build supports diffusion extras.
