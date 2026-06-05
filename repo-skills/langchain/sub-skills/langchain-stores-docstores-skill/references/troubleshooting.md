# Stores Docstores Troubleshooting

## `mget` Returns `None`

Check exact key spelling, tenant prefix, and whether `mset` ran on the same store instance or persistent backend.

## Parent Retriever Cannot Fetch Parents

Confirm child metadata ids match `id_key`, the same docstore was passed to the retriever, and parent docs were added through the retriever or written under matching ids.

## Async Store Code Does Nothing

Use `await store.amset(...)` and `await store.amget(...)`; forgetting `await` leaves coroutine objects unevaluated.

## Data Disappears Between Runs

`InMemoryStore` and `InMemoryByteStore` are not durable. Use a persistent backend for production.

## Serialization Error

Check that stored values match the store type. Byte stores require `bytes`; document stores created with `create_kv_docstore` expect `Document` objects.
