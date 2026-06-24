# Document Loader Workflows

## Local Text Happy Path

1. Install `langchain-community`.
2. Load files with `TextLoader(path, encoding="utf-8")`.
3. Verify each `Document.page_content` is non-empty.
4. Normalize `metadata["source"]` before splitting.
5. Hand off to `RecursiveCharacterTextSplitter` or another splitter.

## Large Corpus Pattern

Use `lazy_load()` when available:

```python
for doc in loader.lazy_load():
    process(doc)
```

Batch downstream splitting/indexing so one large corpus does not live entirely in memory.

## Web Or Cloud Sources

1. Confirm the public loader package and SDK dependency.
2. Validate credentials without printing secrets.
3. Capture stable source ids and permission metadata.
4. Handle rate limits and retries outside the loader when needed.
5. Run a tiny sample before crawling a full source.

## Loader To RAG Handoff

`Document` objects should move through:

```text
loader -> splitter -> embeddings/vector store -> retriever -> LCEL RAG chain
```

Do not embed raw unsplit documents when they exceed the target model context or vector store chunk policy.
