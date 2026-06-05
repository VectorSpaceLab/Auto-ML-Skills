# Retrieval Troubleshooting

- Loader import missing: install `langchain-community` or a dedicated loader package.
- Empty retrieval results: verify documents were added, metadata filters are not too strict, and query embedding dimension matches index dimension.
- Chunk overlap too large: keep `chunk_overlap < chunk_size`.
- RAG prompt sees raw `Document` objects: format documents into strings before the prompt.
- Vector DB connection failure: isolate with `InMemoryVectorStore` first.
- Slow indexing: batch documents and avoid live embedding calls in smoke tests.
