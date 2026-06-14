---
name: langchain-text-splitters-skill
description: "Use when a user wants LangChain text splitting, RecursiveCharacterTextSplitter, token-aware splitting, metadata-preserving chunks, language/code splitters, or chunk-size troubleshooting."
disable-model-invocation: true
---

# LangChain Text Splitters

Use `langchain-text-splitters-skill` after loading documents and before embeddings or indexing. Quick answer: use `RecursiveCharacterTextSplitter`, choose `chunk_size` and `chunk_overlap`, preserve metadata, then validate with `scripts/smoke_text_splitters.py`.

## Short Workflow

1. Confirm `langchain_text_splitters` imports with `../../scripts/check_langchain_env.py`.
2. Start with `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)` for plain text.
3. Use token-aware splitters when the target model's context/token budget matters.
4. Use language/code splitters for source files or Markdown/HTML-aware splitting when structure matters.
5. Run [scripts/smoke_text_splitters.py](scripts/smoke_text_splitters.py) and inspect chunk count, overlap, metadata preservation, and max chunk size.

## Bundled Scripts

- [scripts/smoke_text_splitters.py](scripts/smoke_text_splitters.py): validates recursive splitting over both strings and `Document` objects.

## References

- [references/api-reference.md](references/api-reference.md): splitter imports, parameters, and selection rules.
- [references/workflows.md](references/workflows.md): practical chunking recipes and handoff to vector stores.
- [references/troubleshooting.md](references/troubleshooting.md): overlap, oversized chunks, token drift, and metadata issues.

## Boundaries

Use `langchain-document-loaders-skill` before splitting and `langchain-vectorstores-indexing-skill` after splitting.
