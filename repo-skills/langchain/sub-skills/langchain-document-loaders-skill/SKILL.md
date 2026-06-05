---
name: langchain-document-loaders-skill
description: "Use when a user wants LangChain document loaders, file or web ingestion, lazy loading, blob parsers, metadata handling, loader package boundaries, or no-key loader smoke tests."
disable-model-invocation: true
---

# LangChain Document Loaders

Use `langchain-document-loaders-skill` for ingestion before splitting, embedding, indexing, or RAG. Quick answer: choose the loader package, load to `Document` objects with `page_content` and `metadata`, validate with `scripts/smoke_document_loaders.py`, then route to text splitters or vectorstores.

## Short Workflow

1. For local text ingestion, start with `TextLoader` from `langchain_community.document_loaders` and [scripts/smoke_document_loaders.py](scripts/smoke_document_loaders.py).
2. For PDFs, web pages, cloud files, databases, or SaaS sources, install the documented integration package and confirm credentials separately.
3. Preserve source metadata such as path, URL, page, title, row id, or timestamp before splitting.
4. Prefer lazy loaders for large corpora: `lazy_load()` or streaming iteration before materializing all documents.
5. Read [references/api-reference.md](references/api-reference.md) for public loader classes and [references/workflows.md](references/workflows.md) for ingestion recipes.

## Bundled Scripts

- [scripts/smoke_document_loaders.py](scripts/smoke_document_loaders.py): creates a tiny text file, loads it with `TextLoader`, and verifies `Document` content/metadata without network or credentials.
- [scripts/inspect_loader_requirements.py](scripts/inspect_loader_requirements.py): checks whether common loader integration modules are installed and prints missing-package hints.

## References

- [references/api-reference.md](references/api-reference.md): loader imports, `Document` fields, lazy loading, and package boundaries.
- [references/workflows.md](references/workflows.md): local files, web/cloud loaders, metadata normalization, and handoff to splitting/indexing.
- [references/troubleshooting.md](references/troubleshooting.md): encoding, parsing, credential, network, and loader migration issues.

## Boundaries

Use `langchain-text-splitters-skill` after ingestion, `langchain-vectorstores-indexing-skill` for indexing, and `langchain-retrieval-rag-skill` for retriever/RAG chain wiring.
