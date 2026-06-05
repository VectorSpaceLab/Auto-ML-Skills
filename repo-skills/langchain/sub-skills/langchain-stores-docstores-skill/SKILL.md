---
name: langchain-stores-docstores-skill
description: "Use when a user wants LangChain BaseStore, ByteStore, InMemoryStore, InMemoryByteStore, create_kv_docstore, docstores, parent-document storage, or store serialization troubleshooting."
disable-model-invocation: true
---

# LangChain Stores Docstores

Use `langchain-stores-docstores-skill` when the task involves key-value stores, byte stores, docstores, or parent-document storage. Quick answer: use `InMemoryStore` for generic local KV tests, `InMemoryByteStore` plus `create_kv_docstore` for `Document` storage, and validate with [scripts/smoke_stores_docstores.py](scripts/smoke_stores_docstores.py).

## Short Workflow

1. Decide what is stored:
   - arbitrary Python values: `InMemoryStore`
   - bytes: `InMemoryByteStore`
   - LangChain `Document` objects backed by bytes: `create_kv_docstore`
2. Keep keys stable, string-like, and tenant-scoped when used in production.
3. For `ParentDocumentRetriever` or `MultiVectorRetriever`, use a docstore that can fetch parent documents by stable ids.
4. Avoid unsafe deserialization for untrusted stored bytes.
5. Run [scripts/smoke_stores_docstores.py](scripts/smoke_stores_docstores.py).

## Bundled Scripts

- [scripts/smoke_stores_docstores.py](scripts/smoke_stores_docstores.py): tests `InMemoryStore`, async store methods, `InMemoryByteStore`, and `create_kv_docstore`.
- [scripts/inspect_store_apis.py](scripts/inspect_store_apis.py): reports public store/docstore imports and signatures.

## References

- [references/api-reference.md](references/api-reference.md): store imports, methods, and docstore adapters.
- [references/workflows.md](references/workflows.md): parent-document docstore and local KV recipes.
- [references/troubleshooting.md](references/troubleshooting.md): missing ids, byte serialization, async mistakes, and persistence assumptions.

## Boundaries

Use vectorstores-indexing for embedding indexes. Use advanced retrievers when the store is part of parent/multi-vector retrieval.
