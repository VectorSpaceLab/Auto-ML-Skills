# Document Loaders API Reference

## Core Objects

```python
from langchain_core.documents import Document
```

`Document` has:

- `page_content: str`
- `metadata: dict`
- optional `id` in newer code paths

## Common Loader Imports

```python
from langchain_community.document_loaders import TextLoader
```

Many loaders live in `langchain_community.document_loaders`. Some high-use integrations live in dedicated provider packages. Do not assume a loader is bundled by `langchain` itself.

## Loader Methods

Common loader methods:

- `load() -> list[Document]`: materialize all documents.
- `lazy_load() -> Iterator[Document]`: iterate documents without loading everything into memory.
- async variants may exist on selected loaders, but support is loader-specific.

## Metadata Contract

At ingestion time, normalize metadata keys that downstream retrievers need:

- `source`: file path, URL, or stable external id.
- `page`, `line`, `row`, or `section`: position information when available.
- `title`, `created_at`, `updated_at`, `tenant`, `permissions`: application filters.

Keep metadata JSON-serializable when it will be stored in vector DBs.

## Package Boundaries

- Local text and many community loaders: `langchain-community`.
- Text splitting after loading: `langchain-text-splitters`.
- Provider/cloud specific loaders may require provider packages, service SDKs, credentials, or parser extras.
