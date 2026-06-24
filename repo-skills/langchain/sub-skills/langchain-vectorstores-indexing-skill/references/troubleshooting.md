# Vectorstores And Indexing Troubleshooting

- Dimension mismatch: rebuild the collection or use the same embedding model/dimension.
- Duplicate results: supply stable ids and use an indexing/upsert policy.
- Stale documents remain: define deletion cleanup or record-manager behavior.
- Metadata filters fail: check backend filter syntax and JSON-serializable metadata types.
- No results: verify documents were added, embeddings are non-empty, and `k`/threshold are not too strict.
- Backend import missing: install the dedicated integration package.
- Local smoke tests should not download embedding models; use deterministic fake embeddings.
