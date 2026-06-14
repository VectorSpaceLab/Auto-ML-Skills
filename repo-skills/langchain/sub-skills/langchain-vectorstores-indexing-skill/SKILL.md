---
name: langchain-vectorstores-indexing-skill
description: "Use when a user wants LangChain vector stores, InMemoryVectorStore, indexing API, record managers, retriever search kwargs, Chroma/Qdrant package boundaries, or vector index troubleshooting."
disable-model-invocation: true
---

# LangChain Vectorstores And Indexing

Use `langchain-vectorstores-indexing-skill` for embedding chunks into vector stores, configuring retrievers, and using LangChain indexing helpers. Quick answer for no-key validation: `DeterministicFakeEmbedding`, `InMemoryVectorStore`, `as_retriever`, and `scripts/smoke_vectorstores_indexing.py`.

## Short Workflow

1. Split documents before indexing.
2. For smoke tests, use `DeterministicFakeEmbedding` and `InMemoryVectorStore`.
3. For production stores, install the provider package such as Chroma or Qdrant and record collection/index name, embedding dimension, metric, and persistence/endpoint.
4. Use `as_retriever(search_kwargs={...})` to expose vector search in LCEL/RAG chains.
5. Read [references/api-reference.md](references/api-reference.md) and run [scripts/smoke_vectorstores_indexing.py](scripts/smoke_vectorstores_indexing.py).

## Bundled Scripts

- [scripts/smoke_vectorstores_indexing.py](scripts/smoke_vectorstores_indexing.py): builds a no-key in-memory vector store, queries directly and through a retriever, and checks document ids/metadata.
- [scripts/check_vectorstore_package.py](scripts/check_vectorstore_package.py): import-checks common vector store integration packages.

## References

- [references/api-reference.md](references/api-reference.md): vector store, retriever, indexing, and package-boundary APIs.
- [references/workflows.md](references/workflows.md): no-key index, persistent store setup checklist, retriever tuning.
- [references/troubleshooting.md](references/troubleshooting.md): dimension mismatches, stale indexes, metadata filters, duplicate ids, and backend-specific failures.

## Boundaries

Use document loaders and text splitters before this skill. Use retrieval/RAG skill after a retriever exists.
