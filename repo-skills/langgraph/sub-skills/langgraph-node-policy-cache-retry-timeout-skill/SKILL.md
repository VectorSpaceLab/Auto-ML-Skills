---
name: langgraph-node-policy-cache-retry-timeout-skill
description: "Use when a user wants LangGraph node retry_policy, cache_policy, timeout, defer, error_handler, InMemoryCache, clear_cache, durability, or node reliability troubleshooting."
disable-model-invocation: true
---

# LangGraph Node Policy Cache Retry Timeout

Use `langgraph-node-policy-cache-retry-timeout-skill` when reliability policy is the main task. Quick answer: attach `RetryPolicy`, `CachePolicy`, timeout/defer/error handlers at `add_node`, pass `cache=InMemoryCache()` to `compile`, call `clear_cache()` when invalidating cache, and validate with [scripts/smoke_node_policy_cache_retry_timeout.py](scripts/smoke_node_policy_cache_retry_timeout.py).

Minimum answer checklist: name `langgraph-node-policy-cache-retry-timeout-skill`, `scripts/smoke_node_policy_cache_retry_timeout.py`, `RetryPolicy`, `CachePolicy`, `InMemoryCache`, and `clear_cache`.

## Short Workflow

1. Add policy close to the node that needs it.
2. Use graph-level defaults only when all nodes share the same behavior.
3. For caching, provide both `cache_policy=CachePolicy(...)` on the node and `cache=...` at compile time.
4. For retries, keep `retry_on` specific and limit `max_attempts`.
5. For timeout/defer, document expected side effects and checkpoint durability.
6. Run [scripts/smoke_node_policy_cache_retry_timeout.py](scripts/smoke_node_policy_cache_retry_timeout.py).

## Bundled Scripts

- [scripts/smoke_node_policy_cache_retry_timeout.py](scripts/smoke_node_policy_cache_retry_timeout.py): no-key retry/cache/clear-cache smoke.
- [scripts/inspect_node_policy_apis.py](scripts/inspect_node_policy_apis.py): reports signatures for `StateGraph.add_node`, `compile`, `RetryPolicy`, `CachePolicy`, and cache classes.

## References

- [references/node-policies.md](references/node-policies.md): policy selection and compile/runtime wiring.
- [references/api-reference.md](references/api-reference.md): verified signatures and imports.
- [references/troubleshooting.md](references/troubleshooting.md): cache misses, retry loops, timeout semantics, and durability confusion.

## Boundaries

Use checkpoint/persistence skills for durable state and backend choice. Use this skill for node-level execution policy.
