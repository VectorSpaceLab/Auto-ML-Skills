# Repo-Specific Auto-ML Skills

This directory contains public-ready Codex/agent skill directories extracted and validated for local ML workflows.

## Included Skills

- `llama-factory/`: LLaMA-Factory skill router plus sub-skills for SFT, DPO, PT, RM, KTO, inference, export, API, WebUI, distributed training, and related utilities.
- `flash-rag/`: FlashRAG skill router plus sub-skills for BM25/dense retrieval, sequential and advanced RAG pipelines, generator smoke tests, reranking, evaluation, WebUI, and related utilities.

Each skill directory is self-contained: load the directory containing `SKILL.md` into the agent skill mechanism, then use natural language to request the workflow. The bundled `references/` and `scripts/` files are intended to be used without reopening the original source repositories.
