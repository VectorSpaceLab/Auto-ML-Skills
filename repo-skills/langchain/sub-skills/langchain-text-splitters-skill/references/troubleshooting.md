# Text Splitters Troubleshooting

- Chunks are too large: lower `chunk_size`, add separators, or use token-aware length functions.
- Retrieval misses context: increase overlap, preserve headings, or use parent-document retrieval.
- Too many chunks: increase `chunk_size`, reduce overlap, or filter low-value text before splitting.
- Metadata missing: use `split_documents`, not only `split_text`, or copy metadata explicitly.
- Token count surprises: character chunk sizes do not equal tokenizer sizes.
- Code chunks are broken: use language-aware separators and inspect examples manually.
