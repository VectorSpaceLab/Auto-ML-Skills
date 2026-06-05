# Semantic Store Troubleshooting

## Search Returns Nothing

Check the namespace tuple exactly. `("users", "u1")` and `("users", "u1", "memories")` are different namespaces.

## Memory Does Not Persist

`InMemoryStore` is process-local. Use a durable store backend for production.

## Confused With Checkpoints

Passing `thread_id` to a checkpointer does not write long-term store records. Use `store.put()` or injected store tools.

## TTL Does Not Expire

Confirm the backend supports TTL and that TTL config is enabled. In-memory behavior may differ from production stores.

## Vector Search Missing

Install and configure a backend with index support. Plain `InMemoryStore.search(namespace)` can enumerate namespace items but is not proof of vector ranking.
