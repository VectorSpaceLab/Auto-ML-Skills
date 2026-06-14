# Cache Rate Usage Troubleshooting

## Cache Does Not Hit

Check that the same model instance or global cache scope is used, the prompt is identical, and `cache=False` is not set on the model call.

## Stale Or Wrong Answers

Disable cache for time-sensitive, personalized, or tool-observation prompts. Use scoped cache keys and separate tenant caches in production.

## Rate Limiter Seems To Stall

Inspect `requests_per_second`, `max_bucket_size`, and whether calls are blocking. Use `acquire(blocking=False)` for diagnostics.

## Usage Metadata Is Empty

The callback only aggregates usage when model responses include `AIMessage.usage_metadata` and a model name. Some fake models and providers do not expose token usage.

## Provider Still Bills On Repeated Calls

The cache may be disabled, scoped differently, or bypassed by streaming/tool-call code paths. Validate with fake models before testing against a live provider.
