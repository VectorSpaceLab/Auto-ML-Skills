# Streaming And Async Troubleshooting

- Stream output is not text: check whether chunks are message chunks or parser outputs.
- `asyncio.run` error: the code is already inside an event loop; use `await`.
- Batch rate-limit failures: lower concurrency and add retry/fallback logic.
- No streaming from provider: verify model supports streaming and stream flag/config is enabled if required.
- Event stream too noisy: filter by event name or runnable tags.
