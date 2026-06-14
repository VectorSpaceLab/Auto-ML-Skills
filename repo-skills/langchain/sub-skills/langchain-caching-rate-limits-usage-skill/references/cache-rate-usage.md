# Cache Rate Usage Workflows

## Cache Workflow

1. Decide scope:
   - global: `set_llm_cache(InMemoryCache(...))`
   - model-specific: `FakeListLLM(..., cache=cache)` or provider wrapper equivalent
   - bypass: `cache=False`
2. Validate with the same prompt twice.
3. Check that the second response is cache-backed and does not consume another fake response.
4. Disable or clear cache when prompts include time-sensitive, user-specific, or non-idempotent data.

## Rate Limiter Workflow

1. Start with `InMemoryRateLimiter`.
2. Use low request rates in tests and nonblocking `acquire(blocking=False)` when you need to assert throttle behavior.
3. Attach to model wrappers that accept `rate_limiter`.
4. Remember that cache hits can avoid provider calls and therefore may not need rate limiting.

## Usage Metadata Workflow

```python
from langchain_core.callbacks import get_usage_metadata_callback

with get_usage_metadata_callback() as cb:
    model.invoke("question")
print(cb.usage_metadata)
```

Usage keys are provider/model names when the model response includes them. Always handle an empty result.

## Production Notes

- In-memory caches and rate limiters are process-local.
- Distributed apps need shared caches or provider-side quotas.
- Cache keys include prompt/model details as defined by the model wrapper; changing wrapper versions can change hit behavior.
- Do not cache responses containing secrets or tenant-specific data unless the cache is tenant-scoped.
