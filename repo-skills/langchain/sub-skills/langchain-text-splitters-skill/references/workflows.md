# Text Splitter Workflows

## General RAG Chunking

1. Load documents.
2. Pick chunk size from retriever/model budget, not arbitrary defaults.
3. Split with overlap when answers can cross boundaries.
4. Preserve source/page metadata.
5. Index chunks, not original long documents.

## Metadata Preservation

`split_documents` preserves document metadata by default. Add chunk-specific metadata such as `chunk_id` or `section` after splitting if needed.

## Token-Aware Chunking

When the downstream model or embedding model is token-sensitive, use a token-aware splitter or length function. Validate by measuring actual prompt/context token counts after retrieval, not just splitter character counts.

## Code Or Structured Text

Prefer language/structure-aware separators so chunks do not cut through function definitions, Markdown headings, or HTML blocks when those boundaries matter for retrieval.
