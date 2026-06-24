# Retrieval API Reference

## Documents

```python
from langchain_core.documents import Document
```

Each document has `page_content` and optional `metadata`.

## Text Splitters

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

Use splitters before embedding long documents.

## Embeddings And Vector Stores

```python
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.vectorstores import InMemoryVectorStore
```

Common methods:

- `vector_store.add_documents(docs)`
- `vector_store.similarity_search(query, k=...)`
- `vector_store.as_retriever(search_kwargs={"k": 3})`

## Loaders

Many loaders live in `langchain_community.document_loaders` or provider packages. Install only the loader backend needed by the user.

## Retrievers

Retrievers are runnables. They can be invoked directly or embedded into LCEL chains.
