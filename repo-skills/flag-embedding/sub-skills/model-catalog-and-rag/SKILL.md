---
name: model-catalog-and-rag
description: "Choose FlagEmbedding/BGE model families, resolve common embedder/reranker model_class values, plan instruction-aware retrieval and RAG pipelines, and route concrete implementation work to inference, finetuning, or evaluation sub-skills."
disable-model-invocation: true
---

# Model Catalog And RAG

Use this sub-skill when the task is about selecting a BGE, Qwen3, E5, GTE, or reranker family; deciding whether a model is an embedder or reranker; planning dense/sparse/multi-vector retrieval; or designing a FlagEmbedding-backed RAG workflow before writing implementation code.

## Start Here

1. Identify whether the user needs embedding retrieval, reranking, finetuning, or evaluation.
2. Choose candidate model families from `references/model-catalog.md`.
3. Preserve query instructions and instruction formats when the selected family needs them.
4. For concrete encoding, indexing, scoring, batching, and device code, route to `../inference/`.
5. For training or checkpoint adaptation, route to `../finetuning/`; for benchmarks and retrieval metrics, route to `../evaluation/`.

## Routing Rules

- Use `../inference/` when the next step is loading `FlagAutoModel`, `FlagAutoReranker`, `AbsEmbedder`, or `AbsReranker`, calling `encode_queries`, `encode_corpus`, or `compute_score`, or wiring batches/devices.
- Use `references/model-catalog.md` when deciding model family, `model_class`, pooling expectations, `trust_remote_code`, or instruction templates.
- Use `references/rag-recipes.md` when planning retrieval stages, candidate depth, reranking, BGE-M3 hybrid scoring, or framework integration boundaries.
- Use `references/troubleshooting.md` when auto mapping fails, retrieval quality is weak, BGE-M3 outputs are misunderstood, or optional framework dependencies are missing.
- Use `scripts/recommend_model_class.py` for a safe local lookup of common model basename to embedder/reranker `model_class` without importing FlagEmbedding.

## Core Decisions

- **Embedder first**: choose an embedder for vector search or hybrid retrieval; embedders output vectors or BGE-M3 lexical/multi-vector structures.
- **Reranker second**: choose a reranker for top-k reordering after candidate retrieval; rerankers score `(query, passage)` pairs and do not build the initial vector index.
- **Instructions matter**: pass `query_instruction_for_retrieval` and the right `query_instruction_format` for instruction-tuned models; corpus passages usually do not receive the query instruction.
- **Auto mapping is finite**: when a custom checkpoint is not in auto mapping, specify `model_class` based on the base architecture and family.
- **Framework examples are boundaries**: LangChain, LlamaIndex, vector DB, and notebook examples may require dependencies outside FlagEmbedding; keep FlagEmbedding choices explicit and let framework code own framework-specific setup.

## Quick Helper

```bash
python sub-skills/model-catalog-and-rag/scripts/recommend_model_class.py BAAI/bge-m3
python sub-skills/model-catalog-and-rag/scripts/recommend_model_class.py BAAI/bge-reranker-v2-gemma --kind reranker
python sub-skills/model-catalog-and-rag/scripts/recommend_model_class.py ./my-bge-large-en-v1.5-checkpoint --kind embedder
```

If the helper reports `unknown`, inspect the checkpoint base model, then pass `model_class` explicitly in the concrete inference code.
