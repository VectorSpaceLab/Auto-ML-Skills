---
name: flag-embedding
description: "Use FlagEmbedding/BGE for embedding, reranking, retrieval/RAG model selection, fine-tuning data and command preparation, and evaluation workflow planning."
disable-model-invocation: true
---

# FlagEmbedding

Use this skill when a task involves the FlagEmbedding package or BGE retrieval toolkit: encoding text, reranking query-passage pairs, selecting BGE model families, preparing fine-tuning data/commands, or planning benchmark/custom retrieval evaluation.

## Start Here

1. Install the package for the intended workflow:
   - Inference/evaluation planning: `pip install -U FlagEmbedding`
   - Fine-tuning command execution: `pip install -U "FlagEmbedding[finetune]"` plus the backend packages your hardware supports.
2. Run the minimal import check before giving API advice:
   ```bash
   python - <<'PY'
   import FlagEmbedding
   from FlagEmbedding import FlagAutoModel, FlagAutoReranker
   print('FlagEmbedding import OK')
   PY
   ```
3. For a deeper local diagnostic, run [`scripts/check_install.py`](scripts/check_install.py). It checks imports, package metadata, Torch backend visibility, and optional fine-tune dependencies without downloading models.
4. Read [`references/repo-provenance.md`](references/repo-provenance.md) before deciding whether this skill matches a current checkout. If the commit, package version, or public API surface changed, refresh this skill from the repo.
5. Use [`references/troubleshooting.md`](references/troubleshooting.md) for cross-cutting install/import, dependency, model-download, and hardware issues.

## Route by Task

- **Embedding or reranking inference**: use [`sub-skills/inference/`](sub-skills/inference/) for `FlagAutoModel`, `FlagAutoReranker`, explicit `model_class`, BGE-M3 dense/sparse/ColBERT outputs, reranker normalization, device selection, and inference snippets.
- **Model selection or RAG design**: use [`sub-skills/model-catalog-and-rag/`](sub-skills/model-catalog-and-rag/) for BGE model-family tradeoffs, instruction templates, reranker-vs-embedder choices, RAG pipeline patterns, and auto-mapping troubleshooting.
- **Fine-tuning preparation**: use [`sub-skills/finetuning/`](sub-skills/finetuning/) for JSONL schema validation, hard-negative/teacher-score command planning, data splitting, DeepSpeed config choices, and safe training command construction.
- **Evaluation planning**: use [`sub-skills/evaluation/`](sub-skills/evaluation/) for BEIR, MTEB, MIRACL, MLDR, MKQA, MSMARCO, AIR-Bench, BRIGHT, and custom retrieval evaluation command planning.

## Common Workflow Patterns

- **Quick retrieval prototype**: route to `model-catalog-and-rag` to choose an embedder/reranker pair, then to `inference` for code snippets that encode queries/corpus and rerank top candidates.
- **Custom checkpoint fails auto loading**: route to `model-catalog-and-rag` to identify `model_class`, then to `inference` to pass that class explicitly in `from_finetuned`.
- **Fine-tune then evaluate**: route first to `finetuning` for data validation and training command construction, then to `evaluation` for safe benchmark or custom retrieval command planning.
- **Benchmark request with missing datasets**: route to `evaluation`; produce a command plan and list required caches/credentials instead of running downloads or long benchmarks by default.
- **BGE-M3 score confusion**: route to `inference`; handle dictionary outputs (`dense_vecs`, `lexical_weights`, `colbert_vecs`) instead of assuming every embedder returns a plain matrix.

## Safety Defaults

- Do not run model downloads, long training, distributed launches, benchmark suites, or external dataset downloads unless the user explicitly approves and the environment is prepared.
- Prefer CPU-safe import, parser, and command-builder checks for diagnostics.
- Treat notebook and example content as evidence; use bundled references and scripts in this skill for reusable agent guidance.
- Keep user-provided tokens, private model paths, dataset credentials, cache paths, and local environment paths out of responses and generated artifacts.

## Bundled Shared Script

- [`scripts/check_install.py`](scripts/check_install.py): run when diagnosing package availability, backend selection, optional fine-tune dependencies, or stale installs before routing into a sub-skill.
