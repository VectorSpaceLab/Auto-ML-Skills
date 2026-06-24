# Node Policy Troubleshooting

## Cache Does Not Hit

Check that the node has `cache_policy`, the graph was compiled with `cache=...`, and the input/config used to compute the cache key is stable.

## Retry Does Not Happen

Check `retry_on`. If the thrown exception type is not matched, LangGraph will not retry it.

## Retry Loops Hide Bugs

Keep `max_attempts` small and narrow the exception types. Log attempts during debugging.

## Timeout Behavior Surprises

Timeout behavior depends on sync/async execution and where the node spends time. CPU-bound sync work may not stop at exactly the timeout boundary.

## Deferred Node Runs Too Late

`defer=True` is for end-of-run work. Do not use it for data needed by downstream nodes.
