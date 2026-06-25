---
name: inference
description: "Use FlagEmbedding inference APIs for embedders and rerankers: load models, encode query/corpus text, score BGE-M3 dense/sparse/ColBERT outputs, compute reranker scores, configure devices and precision, and troubleshoot model-loading issues."
disable-model-invocation: true
---

# Inference

Use this sub-skill when a task needs to write or debug FlagEmbedding inference code for embeddings, reranking, or local checkpoint loading. Keep training, fine-tuning commands, benchmark runners, and high-level RAG/model-family strategy in sibling skills.

## Route By Task

- For basic embeddings with `FlagAutoModel`, `FlagModel`, `FlagLLMModel`, `FlagICLModel`, or `FlagPseudoMoEModel`, use `references/workflows.md` and `references/api-reference.md`.
- For BGE-M3 dense, sparse, and ColBERT outputs, use `references/workflows.md` and check whether downstream code expects a dictionary or a plain array.
- For reranking with `FlagAutoReranker`, `FlagReranker`, `FlagLLMReranker`, `LayerWiseFlagLLMReranker`, or `LightWeightFlagLLMReranker`, use `references/workflows.md`.
- For explicit `model_class`, pooling, instruction templates, precision, devices, and max-length choices, use `references/model-selection.md`.
- For import/backend checks that do not download models, run `scripts/check_inference_env.py`.
- For deterministic starter code that does not download models while generating snippets, run `scripts/build_inference_snippet.py`.
- For loading failures, cache/network/token issues, unsupported precision, unexpected devices, BGE-M3 output shape mismatches, or layerwise/lightweight reranker arguments, use `references/troubleshooting.md`.

## Fast Rules

- Prefer `FlagAutoModel.from_finetuned(...)` or `FlagAutoReranker.from_finetuned(...)` for released mapped checkpoints.
- Pass `model_class` explicitly for local or renamed checkpoints that are not in the auto mappings.
- Use `encode_queries()` for retrieval queries when query instructions are configured; use `encode_corpus()` for passages.
- Expect normal embedders to return an ndarray/tensor, but BGE-M3 to return a dict with keys such as `dense_vecs`, `lexical_weights`, and `colbert_vecs` depending on flags.
- Set `devices="cpu"` and `use_fp16=False` for CPU-safe examples unless the caller intentionally targets GPU/NPU/MPS/MUSA hardware.

## References

- `references/api-reference.md`: constructor arguments, methods, class names, and return conventions.
- `references/workflows.md`: copyable embedder, BGE-M3, reranker, layerwise, and custom checkpoint workflows.
- `references/model-selection.md`: auto mapping, explicit classes, device/precision, instructions, pooling, and truncation choices.
- `references/troubleshooting.md`: symptoms, causes, and fixes for common inference failures.
