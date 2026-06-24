# Troubleshooting

## Troubleshooting

- `No module named Stemmer`: install `PyStemmer`; the import name is `Stemmer`.
- `No module named bm25s`: install `bm25s[core]==0.2.1`.
- `No module named faiss`: use this skill's BM25 scripts, or install `faiss-cpu` if you import FlashRAG retriever modules directly.
- `No module named langid`: use this skill's BM25 scripts for English smoke tests, or install `langid` for automatic Chinese/English detection.
- Empty or irrelevant results: confirm the query language matches the corpus and that the same corpus path is used for both index build and retrieval config.
- `FileNotFoundError` for index files: remember the builder writes to `<save-dir>/bm25`, not directly to `<save-dir>`.
- Chinese corpora: FlashRAG chooses a Chinese tokenizer when `langid` detects Chinese in the first document, but the source notes BM25s Chinese support is limited.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-bm25-retrieval-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

