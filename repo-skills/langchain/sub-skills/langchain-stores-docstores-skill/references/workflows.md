# Stores Docstores Workflows

## Generic KV Store

```python
from langchain_core.stores import InMemoryStore

store = InMemoryStore()
store.mset([("tenant:user:fact", {"fact": "prefers concise answers"})])
facts = store.mget(["tenant:user:fact"])
```

Use this for local tests and simple process-local state.

## Parent Document Docstore

```python
from langchain_classic.storage import create_kv_docstore
from langchain_core.stores import InMemoryByteStore

docstore = create_kv_docstore(InMemoryByteStore())
```

Pass `docstore` to `ParentDocumentRetriever` so child vector hits can fetch full parent documents.

## Key Design

Prefer keys that encode:

- tenant or user id
- source id
- document or record id
- version when updates are expected

Avoid raw user text as keys.

## Serialization Safety

Only deserialize stored bytes from trusted stores. If a legacy store adapter supports richer LangChain serialization, treat it as trusted-data only unless the reference explicitly says it is safe for untrusted input.
