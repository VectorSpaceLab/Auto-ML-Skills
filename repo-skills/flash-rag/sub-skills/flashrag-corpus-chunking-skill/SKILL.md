---
name: flashrag-corpus-chunking-skill
description: "Use when a user wants FlashRAG Corpus chunking and long-document passage preparation."
disable-model-invocation: true
---

# Corpus chunking and long-document passage preparation.

Use this sub-skill after the root `flash-rag` router selects `flashrag-corpus-chunking-skill`. It is focused on one workflow family and should be enough to validate inputs, generate/adapt configs, run a smoke test, inspect outputs, and then scale to the user's requested run without reopening the original repository docs.

## Short Workflow

1. Confirm the public package environment with the root script `../../scripts/check_flash_rag_env.py`.
2. Resolve user-provided model/data/corpus/output paths and choose smoke or full scale.
3. Read [references/workflows.md](references/workflows.md) for the detailed flow and placeholders to fill.
4. Read [references/data.md](references/data.md) for inputs, configs, and decision points.
5. Run or adapt the bundled helper scripts below; each script is inside this sub-skill directory.
6. Launch real work through installed FlashRAG package APIs or `python -m flashrag.retriever.index_builder` for index building; do not use private source checkout paths.
7. Inspect outputs, save logs/configs/summaries, and report `valid: true/false` with concrete artifact paths.

## Bundled Scripts

- [scripts/check_env.py](scripts/check_env.py): bundled helper; run `python scripts/check_env.py --help` before use.
- [scripts/chunk_corpus.py](scripts/chunk_corpus.py): bundled helper; run `python scripts/chunk_corpus.py --help` before use.
- [scripts/inspect_chunks.py](scripts/inspect_chunks.py): bundled helper; run `python scripts/inspect_chunks.py --help` before use.
- [scripts/validate_doc_corpus.py](scripts/validate_doc_corpus.py): bundled helper; run `python scripts/validate_doc_corpus.py --help` before use.

## References

- [references/workflows.md](references/workflows.md): detailed end-to-end workflow distilled from the extracted skill.
- [references/data.md](references/data.md): configuration, data, CLI, or workflow details nearest to this sub-skill.
- [references/troubleshooting.md](references/troubleshooting.md): sub-skill-specific and general failure handling.

## Boundaries

This sub-skill does not own unrelated FlashRAG capabilities. Return to the root router when the user asks for a different stage, backend, pipeline, service, or evaluation family.
