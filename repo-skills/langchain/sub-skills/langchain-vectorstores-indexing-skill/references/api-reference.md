# Vectorstores And Indexing API Reference

## No-Key Imports

```python
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.vectorstores import InMemoryVectorStore
```

## Common Methods

- `store.add_documents(documents, ids=None)`
- `store.similarity_search(query, k=...)`
- `store.similarity_search_with_score(query, k=...)`
- `store.as_retriever(search_kwargs={"k": ...})`

## Indexing Module

`langchain_core.indexing` contains indexing helpers and record-manager concepts for avoiding duplicate or stale writes. API details vary by version; inspect with root `scripts/inspect_langchain_api.py` when using it directly.

## Integration Packages

Examples:

- Chroma: install a Chroma integration package and the Chroma backend requirements.
- Qdrant: install the Qdrant integration package and configure URL/API key or local mode.
- Other stores: install the dedicated provider package; do not assume it is part of `langchain`.

Always align embedding model and vector dimension with the store collection.
