---
name: langchain-retrieval-rag-skill
description: "Use when a user wants LangChain retrieval, RAG, vector stores, retrievers, text splitters, document loaders, indexing, or no-key retrieval smoke tests."
disable-model-invocation: true
---

# LangChain Retrieval And RAG

Use this sub-skill for document preparation, vector store indexing, retriever wiring, and RAG chain debugging.

## Short Workflow

1. Confirm package imports with `../../scripts/check_langchain_env.py`.
2. For a no-key smoke workflow, name `DeterministicFakeEmbedding`, `InMemoryVectorStore`, and [scripts/smoke_retrieval.py](scripts/smoke_retrieval.py) explicitly.
3. Read [references/api-reference.md](references/api-reference.md) for documents, splitters, vector stores, retrievers, and loaders.
4. Read [references/workflows.md](references/workflows.md) for no-key indexing and RAG composition.
5. Run [scripts/smoke_retrieval.py](scripts/smoke_retrieval.py) before introducing real embedding providers or vector DBs.

## Bundled Scripts

- [scripts/smoke_retrieval.py](scripts/smoke_retrieval.py): builds a tiny in-memory vector store with deterministic embeddings and queries it.

## References

- [references/api-reference.md](references/api-reference.md): retrieval primitives and package boundaries.
- [references/workflows.md](references/workflows.md): RAG and indexing patterns.
- [references/troubleshooting.md](references/troubleshooting.md): loader, splitter, vector store, and retriever failures.

## Boundaries

Use model, prompt/parser, LCEL, memory, structured output, or observability sub-skills when retrieval is only one stage in a larger chain.
