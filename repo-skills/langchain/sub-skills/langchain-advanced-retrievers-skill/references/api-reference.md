# Advanced Retriever API Reference

Read this when configuring advanced retriever classes.

## Imports

Many advanced retrievers live in `langchain_classic` or `langchain_community` even when used in modern LangChain apps:

```python
from langchain_classic.retrievers import (
    ContextualCompressionRetriever,
    EnsembleRetriever,
    MultiQueryRetriever,
    MultiVectorRetriever,
    ParentDocumentRetriever,
    SelfQueryRetriever,
    TimeWeightedVectorStoreRetriever,
)
```

Lexical community retrievers such as `BM25Retriever` may require `langchain-community` and optional packages.

## Verified Constructor Shapes

| Class | Key parameters |
| --- | --- |
| `MultiQueryRetriever` | `retriever`, `llm_chain`, `verbose=True`, `parser_key="lines"`, `include_original=False` |
| `ContextualCompressionRetriever` | `base_compressor`, `base_retriever` |
| `EnsembleRetriever` | `retrievers`, `weights`, `c=60`, `id_key=None` |
| `ParentDocumentRetriever` | `vectorstore`, `docstore`, `child_splitter`, optional `parent_splitter`, `id_key="doc_id"` |
| `MultiVectorRetriever` | `vectorstore`, `docstore` or `byte_store`, `id_key="doc_id"`, `search_kwargs`, `search_type` |
| `SelfQueryRetriever` | `vectorstore`, `llm_chain`, `structured_query_translator`, `search_type`, `search_kwargs`, `use_original_query` |

## Parent Document Retriever

Use when embeddings should be built on small child chunks but retrieval should return larger parent documents:

```python
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import create_kv_docstore
from langchain_core.stores import InMemoryByteStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

docstore = create_kv_docstore(InMemoryByteStore())
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40),
)
retriever.add_documents(parent_docs)
docs = retriever.invoke("question")
```

## Ensemble Retriever

Use when combining vector, lexical, metadata, or custom retrievers:

```python
from langchain_classic.retrievers import EnsembleRetriever

hybrid = EnsembleRetriever(
    retrievers=[vector_retriever, lexical_retriever],
    weights=[0.6, 0.4],
    id_key="source_id",
)
```

Set `id_key` when the same logical document appears from several retrievers and metadata contains a stable id.

## Self Query Boundary

`SelfQueryRetriever` requires a vector store translator for the backend's filter syntax and an LLM chain that returns a `StructuredQuery`. Treat it as a metadata-filtering workflow, not as a generic reranker.

## Compression Boundary

`ContextualCompressionRetriever` runs a base retriever, then a document compressor. Compressors may be LLM-backed, embedding-backed, or reranker-backed. Validate base retriever recall before compression, otherwise the compressor cannot recover missing documents.
