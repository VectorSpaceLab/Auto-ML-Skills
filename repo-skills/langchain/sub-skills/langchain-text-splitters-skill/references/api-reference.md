# Text Splitters API Reference

## Core Imports

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
```

## Common Parameters

- `chunk_size`: target maximum chunk size in splitter units.
- `chunk_overlap`: overlap between adjacent chunks.
- `separators`: ordered separators for recursive splitting.
- `keep_separator`: keep separators at start/end or drop them.
- `is_separator_regex`: interpret separators as regex patterns.

## Common Methods

- `split_text(text) -> list[str]`
- `split_documents(documents) -> list[Document]`
- `create_documents(texts, metadatas=None) -> list[Document]`

## Splitter Selection

- General prose: `RecursiveCharacterTextSplitter`.
- Code: language-aware splitters and separators when available.
- Markdown/HTML: structure-aware splitters before fallback recursive splitting.
- Token budgets: token-aware constructors or token-length functions.
