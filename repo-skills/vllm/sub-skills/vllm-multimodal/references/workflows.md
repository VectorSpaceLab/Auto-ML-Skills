# Multimodal Workflows

## Planning

1. Identify modality: image, video, audio, speech, or prompt embeddings.
2. Choose a vLLM-supported model for that modality.
3. Confirm prompt placeholders or chat template requirements.
4. Validate media paths/URLs before model loading.
5. Smoke with one small media item and short output.

## OpenAI Chat Image Payload

```json
{
  "model": "MODEL_ID",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image briefly."},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
      ]
    }
  ],
  "max_tokens": 64
}
```

## Offline

Offline multimodal inputs may use prompt dictionaries and `multi_modal_data` depending on model and installed vLLM version. Prefer the model's documented input processor shape and inspect errors carefully.

## Speech

Current vLLM entrypoints include speech-to-text transcription/translation/realtime modules. Endpoint support depends on model and version; inspect CLI help and server routes before relying on them.
