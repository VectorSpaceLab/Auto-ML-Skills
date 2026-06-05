# Multimodal Reference

## Media Forms

- HTTP(S) image URLs in OpenAI chat content.
- Data URLs/base64 where supported by server and client constraints.
- Local paths for offline code, never for remote clients unless served.
- Audio/video payloads require model-specific support and may require extra dependencies.
- Speech-to-text endpoints use file upload or realtime audio events rather than normal chat content.

## Prompt Placeholder Issues

Many vision-language models need placeholder tokens such as image markers in the chat template. If the model errors on placeholder count, verify:

- Prompt contains the right media marker.
- The number of media items matches placeholder count.
- Processor kwargs are compatible with model limits.
- `max-model-len` is high enough for expanded media tokens.

## Tuning Notes

Multimodal processing can dominate latency. Benchmark media preprocessing separately with `vllm bench mm-processor` when optimizing.

## Audio And Realtime

Install public audio extras when using ASR or realtime transcription, for example `uv pip install 'vllm[audio]'` in the target environment.

Endpoint families:

- `/v1/audio/transcriptions`: ASR transcription for supported models.
- `/v1/audio/translations`: translation for supported ASR models.
- WebSocket `/v1/realtime`: streaming transcription for realtime-capable ASR models.

Realtime audio should be base64-encoded PCM16, 16 kHz, mono. The usual event sequence is:

1. Connect to `ws://host/v1/realtime`.
2. Receive `session.created`.
3. Optionally send `session.update` with model/settings.
4. Send `input_audio_buffer.append` events.
5. Send `input_audio_buffer.commit`.
6. Read `transcription.delta`, `transcription.done`, or `error` events.

Do not route realtime ASR work through text-generation chat payloads.

## Prompt Embeddings

Some workflows pass prompt embeddings or multimodal embeddings directly in offline inputs. Treat these as model-specific offline payloads, not OpenAI-compatible JSON. Validate tensor shape, dtype, device placement, and placeholder-token alignment before model loading.
