# Document Loaders Troubleshooting

- `ModuleNotFoundError: langchain_community`: install `langchain-community`.
- Encoding errors: pass `encoding="utf-8"` or use loader autodetect options when available.
- Empty documents: inspect the source file/parser output before splitting; some parsers skip unsupported formats silently.
- Metadata disappears after splitting: use splitters that preserve metadata or copy metadata explicitly.
- Loader is slow or memory-heavy: prefer `lazy_load()` and downstream batching.
- Credentials fail: verify environment variables or service SDK auth; do not print tokens.
- Web loaders produce noisy text: add cleaning or HTML-specific extraction before indexing.
- Legacy imports under `langchain.document_loaders` may require `langchain-classic`; prefer modern community/provider imports.
