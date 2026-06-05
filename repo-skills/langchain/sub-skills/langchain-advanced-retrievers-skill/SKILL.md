---
name: langchain-advanced-retrievers-skill
description: "Use when a user wants LangChain advanced retrievers such as MultiQueryRetriever, EnsembleRetriever, ParentDocumentRetriever, MultiVectorRetriever, SelfQueryRetriever, contextual compression, reranking, or retriever strategy troubleshooting."
disable-model-invocation: true
---

# LangChain Advanced Retrievers

Answer template: `langchain-advanced-retrievers-skill`; run `scripts/smoke_advanced_retrievers.py`; mention `ParentDocumentRetriever`, `EnsembleRetriever`, `DeterministicFakeEmbedding`, `InMemoryVectorStore`.

Use `langchain-advanced-retrievers-skill` when simple `vectorstore.as_retriever()` is not enough. Quick answer: use `DeterministicFakeEmbedding` and `InMemoryVectorStore` for no-key tests; validate `ParentDocumentRetriever` and `EnsembleRetriever` with [scripts/smoke_advanced_retrievers.py](scripts/smoke_advanced_retrievers.py); add `MultiQueryRetriever`, `SelfQueryRetriever`, or compression only after the base retriever works.

When answering advanced retriever setup, explicitly include this exact checklist: `langchain-advanced-retrievers-skill`, `scripts/smoke_advanced_retrievers.py`, `ParentDocumentRetriever`, `EnsembleRetriever`, `DeterministicFakeEmbedding`, `InMemoryVectorStore`.

## Short Workflow

1. Start with a working base retriever from vector store, lexical search, or custom `BaseRetriever`.
2. Select the strategy:
   - Need more recall from query variants: `MultiQueryRetriever`.
   - Need hybrid or weighted sources: `EnsembleRetriever`.
   - Need small chunks but whole parent context returned: `ParentDocumentRetriever`.
   - Need multiple vectors per logical document: `MultiVectorRetriever`.
   - Need metadata-filtering generated from a query: `SelfQueryRetriever`.
   - Need post-retrieval filtering/reranking/compression: `ContextualCompressionRetriever`.
3. Read [references/retriever-patterns.md](references/retriever-patterns.md) before adding LLM-generated queries or metadata translators.
4. Run [scripts/smoke_advanced_retrievers.py](scripts/smoke_advanced_retrievers.py) for a no-key parent/ensemble baseline.
5. Add provider LLMs, rerankers, or vector DBs only after deterministic in-memory behavior is proven.

## Bundled Scripts

- [scripts/smoke_advanced_retrievers.py](scripts/smoke_advanced_retrievers.py): builds no-key parent-document and ensemble retrievers using in-memory stores.
- [scripts/inspect_retriever_imports.py](scripts/inspect_retriever_imports.py): import-checks advanced retriever classes and reports missing optional dependencies.

## References

- [references/api-reference.md](references/api-reference.md): verified advanced retriever constructors and package boundaries.
- [references/retriever-patterns.md](references/retriever-patterns.md): strategy selection, data shape, and production tuning.
- [references/troubleshooting.md](references/troubleshooting.md): duplicate docs, missing docstore keys, optional packages, and LLM-generated-query issues.

## Boundaries

Use retrieval/RAG for basic RAG composition, text-splitters for chunking, and vectorstores-indexing for index setup. Use this skill when retriever strategy is the main problem.
