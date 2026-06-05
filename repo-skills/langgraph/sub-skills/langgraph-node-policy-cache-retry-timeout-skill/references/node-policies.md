# Node Policies

## Policy Selection

| Need | Policy |
| --- | --- |
| Transient failure recovery | `RetryPolicy` |
| Reuse deterministic node output | `CachePolicy` plus compile-time cache |
| Stop slow nodes | node `timeout` |
| Run cleanup/finalization near the end | `defer=True` |
| Convert node exceptions into state updates | `error_handler` |

## Retry Workflow

1. Identify the exact transient exception.
2. Set small `max_attempts` in smoke tests.
3. Use `initial_interval=0` and `jitter=False` for deterministic tests.
4. Make side effects idempotent before retrying a node.

## Cache Workflow

1. Add `cache_policy` to deterministic nodes only.
2. Compile with a cache object.
3. Re-run the same input and confirm the cached node did not execute again.
4. Clear cache when upstream model/config/data changes.

## Durability Boundary

`durability` controls checkpoint write timing for checkpointed graphs; cache policy controls node output reuse. They solve different problems.

## Side Effects

Never cache or retry a node that mutates external state unless the mutation is idempotent or externally guarded.
