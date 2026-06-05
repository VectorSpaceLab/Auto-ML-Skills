# Multimodal Serving Reference

## Vision Chat Payload

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:30000/v1", api_key="None")
resp = client.chat.completions.create(
    model="<VLM_MODEL_ID>",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image in one sentence."},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
        ],
    }],
    max_tokens=64,
)
```

SGLang docs/examples cover image, multi-image, and video payloads for Llava/Qwen/Pixtral-style models. Hardware requirements are model-specific; do not assume a text-only smoke model can handle vision.

Video chat uses OpenAI-style `video_url` blocks when the model supports video:

```python
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "What is happening in this clip?"},
        {"type": "video_url", "video_url": {"url": "https://example.com/clip.mp4"}},
    ],
}]
```

## Native Multimodal `/generate`

Native request fields include:

- `image_data`: PIL image, file path, URL, base64 string, processor output dict, or precomputed embedding dict.
- `audio_data`: file name, URL, or base64 string.
- `video_data`: file path, URL, base64 string, or processor-supported video object.
- `text` with model-specific placeholder tokens/templates when required.

The language frontend exposes `sgl.image(...)` and `sgl.video(path, num_frames)` for multimodal prompts.

## Multimodal Embeddings

Use an embedding-capable multimodal model and start server with embedding mode when required:

```bash
python -m sglang.launch_server --model-path <MULTIMODAL_EMBEDDING_MODEL_ID> --is-embedding --host 127.0.0.1 --port 30000
```

Then use `/v1/embeddings` or native `/encode` depending on client needs.

## Audio And ASR

Inspected OpenAI-compatible routes include `/v1/audio/transcriptions` and websocket `/v1/realtime` for transcription/realtime flows. The realtime route implements transcription behavior. ServerArgs include ASR controls such as `asr_max_buffer_seconds` and `asr_max_concurrent_sessions`.

## Diffusion

The CLI dispatches standard LLM serving or diffusion serving through `sglang serve`; optional `--model-type {auto,llm,diffusion}` can force dispatch. Diffusion extras are optional package dependencies and may not be installed.

Patterns:

```bash
sglang serve --model-path <DIFFUSION_MODEL_ID> --model-type diffusion --host 127.0.0.1 --port 30000
sglang generate --model-path <DIFFUSION_MODEL_ID> --prompt "a clean product photo" --save-output
```

Check `sglang generate --help` in the target environment before writing exact diffusion flags, because they are model/pipeline-specific.

Diffusion-specific environment variables include target device, attention backend/config, stage logging, profiler directory, cache/config roots, worker multiprocessing method, Run:AI streaming, Cache-DiT controls, and optional S3-compatible cloud storage settings. Keep generated commands model/pipeline-specific rather than copying every env var.
