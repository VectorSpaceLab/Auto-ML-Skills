# Stores Docstores API Reference

## Core Imports

```python
from langchain_core.stores import InMemoryByteStore, InMemoryStore
from langchain_classic.storage import create_kv_docstore
```

Verified signatures:

```text
InMemoryStore()
InMemoryByteStore()
create_kv_docstore(store, *, key_encoder=None)
```

## InMemoryStore

Use for process-local key-value tests:

```python
store = InMemoryStore()
store.mset([("a", {"score": 1})])
values = store.mget(["a"])
keys = list(store.yield_keys())
store.mdelete(["a"])
```

Async counterparts such as `amset`, `amget`, `amdelete`, and `ayield_keys` are available on the base interface.

## InMemoryByteStore

Use when the backing store stores bytes:

```python
byte_store = InMemoryByteStore()
byte_store.mset([("raw", b"value")])
```

## Document Store Adapter

`create_kv_docstore` adapts a byte store into a document store:

```python
from langchain_core.documents import Document

docstore = create_kv_docstore(InMemoryByteStore())
docstore.mset([("doc-1", Document(page_content="text", metadata={"source": "demo"}))])
doc = docstore.mget(["doc-1"])[0]
```

This is commonly used by `ParentDocumentRetriever` and `MultiVectorRetriever`.

## Persistence Boundary

In-memory stores are process-local and not durable. For persistent storage, pick a backend integration and document serialization format explicitly.
