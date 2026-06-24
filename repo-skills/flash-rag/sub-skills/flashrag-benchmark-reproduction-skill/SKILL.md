---
name: flashrag-benchmark-reproduction-skill
description: "Use when a user wants FlashRAG benchmark reproduction, unified method settings, reproduce_experiment guidance, method-specific extra models, or result-alignment checks."
disable-model-invocation: true
---

# FlashRAG Benchmark Reproduction

Use this sub-skill when the user wants to reproduce FlashRAG benchmark methods, align with the public baseline setup, decide which extra models a method needs, or prepare a reproducible `my_config.yaml` equivalent.

## Short Workflow

1. Confirm the base assets: generator model, retriever model, datasets, corpus JSONL, and retrieval indexes.
2. Use [scripts/make_reproduction_config.py](scripts/make_reproduction_config.py) to generate a self-contained config skeleton for the user's local asset paths.
3. Use [scripts/method_dependency_matrix.py](scripts/method_dependency_matrix.py) to identify extra model/index/training-data requirements for the selected method.
4. For index creation, route to `flashrag-dense-retrieval-skill`, `flashrag-bm25-retrieval-skill`, or `flashrag-multimodal-index-skill`.
5. Run the chosen method through installed FlashRAG APIs or a bundled/adapted runner, not by assuming original example files exist.
6. Inspect predictions and metric outputs with the nearest evaluation scripts, then compare settings before comparing scores.

Read [references/reproduction.md](references/reproduction.md) for the unified benchmark setup. Read [references/method-dependencies.md](references/method-dependencies.md) for method-specific extra assets. Read [references/troubleshooting.md](references/troubleshooting.md) for reproducibility drift and path issues.

## Scripts

- [scripts/make_reproduction_config.py](scripts/make_reproduction_config.py): emits a baseline FlashRAG reproduction YAML skeleton.
- [scripts/method_dependency_matrix.py](scripts/method_dependency_matrix.py): prints method-specific extra dependencies and caveats.

## Boundaries

Use `flashrag-methods-runner-skill` for per-method command construction and fake smoke tests. Use retrieval/index sub-skills when the missing artifact is an index rather than a method config.
