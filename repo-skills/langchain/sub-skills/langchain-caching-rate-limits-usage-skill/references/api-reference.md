# Cache Rate Usage API Reference

Read this for verified imports and API shapes.

## Cache

```python
from langchain_core.caches import InMemoryCache
from langchain_core.globals import get_llm_cache, set_llm_cache
```

Verified signatures:

```text
InMemoryCache(*, maxsize: int | None = None)
set_llm_cache(value)
get_llm_cache()
```

Use:

```python
cache = InMemoryCache(maxsize=128)
set_llm_cache(cache)
```

Many model wrappers also accept `cache=cache`, `cache=True`, `cache=False`, or `cache=None` depending on class.

## Rate Limiter

```python
from langchain_core.rate_limiters import InMemoryRateLimiter
```

Verified signature:

```text
InMemoryRateLimiter(requests_per_second=1, check_every_n_seconds=0.1, max_bucket_size=1)
```

Methods:

```python
limiter.acquire(blocking=True)
await limiter.aacquire(blocking=True)
```

Attach to chat models that accept `rate_limiter=...`.

## Usage Metadata

```python
from langchain_core.callbacks import UsageMetadataCallbackHandler, get_usage_metadata_callback
```

Usage is aggregated from `AIMessage.usage_metadata` and `response_metadata["model_name"]` when present. Providers that do not populate usage metadata cannot be counted by this callback without wrapper-specific support.

## Fake Model Smoke Imports

```python
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.language_models.fake_chat_models import FakeListChatModel
```

Fake models are suitable for cache behavior and callback plumbing tests without API keys.
