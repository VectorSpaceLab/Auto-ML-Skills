# Multimodal Reference

## Media Forms

- HTTP(S) image URLs in OpenAI chat content.
- Data URLs/base64 where supported by server and client constraints.
- Local paths for offline code, never for remote clients unless served.
- Audio/video payloads require model-specific support and may require extra dependencies.

## Prompt Placeholder Issues

Many vision-language models need placeholder tokens such as image markers in the chat template. If the model errors on placeholder count, verify:

- Prompt contains the right media marker.
- The number of media items matches placeholder count.
- Processor kwargs are compatible with model limits.
- `max-model-len` is high enough for expanded media tokens.

## Tuning Notes

Multimodal processing can dominate latency. Benchmark media preprocessing separately with `vllm bench mm-processor` when optimizing.
