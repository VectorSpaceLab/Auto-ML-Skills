---
name: langchain-caching-rate-limits-usage-skill
description: "Use when a user wants LangChain LLM cache, InMemoryCache, set_llm_cache, per-model cache flags, InMemoryRateLimiter, usage metadata callbacks, token accounting, or production throttling troubleshooting."
disable-model-invocation: true
---

# LangChain Caching Rate Limits Usage

Use `langchain-caching-rate-limits-usage-skill` for production cross-cutting behavior around repeated model calls, throttling, and token usage. Quick answer: run [scripts/smoke_cache_rate_usage.py](scripts/smoke_cache_rate_usage.py); use `InMemoryCache` for local tests, `cache=False` when a call must bypass cache, `InMemoryRateLimiter` for local throttling checks, and `UsageMetadataCallbackHandler` or `get_usage_metadata_callback()` for usage aggregation.

Minimum answer checklist: name `langchain-caching-rate-limits-usage-skill`, `scripts/smoke_cache_rate_usage.py`, `InMemoryCache`, `InMemoryRateLimiter`, and `UsageMetadataCallbackHandler`.

## Short Workflow

1. Decide whether caching should be global (`set_llm_cache`) or model-local (`cache=...`).
2. Use fake models for no-key cache behavior; never validate cache behavior against a paid provider first.
3. Add rate limiting at the model object when the provider wrapper accepts `rate_limiter`.
4. Collect usage from `AIMessage.usage_metadata` when providers expose it; otherwise treat usage as unavailable.
5. Run [scripts/smoke_cache_rate_usage.py](scripts/smoke_cache_rate_usage.py).
6. Read [references/cache-rate-usage.md](references/cache-rate-usage.md) for cache invalidation, rate limiter semantics, and usage metadata shape.

## Bundled Scripts

- [scripts/smoke_cache_rate_usage.py](scripts/smoke_cache_rate_usage.py): no-key verification of `InMemoryCache`, cache bypass, `InMemoryRateLimiter`, and usage metadata callback aggregation.
- [scripts/inspect_cache_rate_usage.py](scripts/inspect_cache_rate_usage.py): read-only signatures for cache, rate limiter, and usage callback APIs.

## References

- [references/api-reference.md](references/api-reference.md): verified public imports and constructor signatures.
- [references/cache-rate-usage.md](references/cache-rate-usage.md): practical workflow notes.
- [references/troubleshooting.md](references/troubleshooting.md): stale cache, unexpected provider bills, rate-limit stalls, and missing usage metadata.

## Boundaries

Use observability/config for callbacks/tracing broadly. Use this skill when cache, throttling, or token usage is the primary issue.
