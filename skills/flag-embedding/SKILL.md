---
name: flag-embedding
description: "Helps agents use FlagEmbedding for BGE embedding inference, reranking, fine-tuning, evaluation, and retrieval data preparation."
disable-model-invocation: true
---

# FlagEmbedding

Use this repo skill when a task involves the `FlagEmbedding` Python package, BGE embedders, BGE rerankers, retrieval data preparation, fine-tuning, or benchmark evaluation.

FlagEmbedding is a retrieval toolkit for Search and RAG. The public package exposes embedders, rerankers, training module entry points, evaluation module entry points, and helper workflows for hard-negative mining, teacher scoring, and sequence-length splitting.

## Install

For inference and evaluation basics:

```bash
python -m pip install -U FlagEmbedding
```

For fine-tuning:

```bash
python -m pip install -U "FlagEmbedding[finetune]"
```

The package metadata requires `torch`, `transformers>=4.44.2,<6.0.0`, `datasets>=2.19.0`, `accelerate>=0.20.1`, `sentence_transformers`, `peft`, `ir-datasets`, `sentencepiece`, and `protobuf`. Fine-tuning extras add `deepspeed` and `flash-attn`.

Run this import check before giving a detailed workflow:

```bash
python - <<'PY'
import FlagEmbedding
print("FlagEmbedding import OK")
print([name for name in ["FlagAutoModel", "FlagAutoReranker", "BGEM3FlagModel"] if hasattr(FlagEmbedding, name)])
PY
```

For a more complete local check that avoids model downloads, run [scripts/check_flag_embedding_env.py](scripts/check_flag_embedding_env.py).

## Sub-Skills

Use [sub-skills/inference/SKILL.md](sub-skills/inference/SKILL.md) for embedding vectors, M3 dense/sparse/ColBERT outputs, query/passage scoring, cross-encoder reranking, LLM rerankers, layerwise rerankers, lightweight rerankers, custom model-class selection, and inference API signatures.

Use [sub-skills/finetuning/SKILL.md](sub-skills/finetuning/SKILL.md) for `torchrun -m FlagEmbedding.finetune...` workflows, embedder training, reranker training, LoRA arguments, DeepSpeed configs, training JSONL schemas, and distillation fields.

Use [sub-skills/evaluation/SKILL.md](sub-skills/evaluation/SKILL.md) for `python -m FlagEmbedding.evaluation...` commands, MTEB, BEIR, MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, and custom retrieval datasets.

Use [sub-skills/data-preparation/SKILL.md](sub-skills/data-preparation/SKILL.md) for hard-negative mining, adding reranker teacher scores, splitting training data by token length, and validating retrieval JSONL files.

## Repo-Level References

Read [references/package-overview.md](references/package-overview.md) when you need public package facts, installation variants, dependency notes, exported top-level classes, and module-entry-point overview.

Read [references/model-overview.md](references/model-overview.md) when choosing `FlagAutoModel` or `FlagAutoReranker` model names, `model_class` values, pooling methods, trust-remote-code defaults, query-instruction formats, and model family tradeoffs.

Read [references/troubleshooting.md](references/troubleshooting.md) when imports fail, Hugging Face model loading fails, CUDA/precision choices are unclear, evaluation dependencies are missing, or auto model mapping rejects a local checkpoint.

## Repo-Level Scripts

Run [scripts/check_flag_embedding_env.py](scripts/check_flag_embedding_env.py) to verify importability, installed package metadata, exported classes, auto-mapping names, and API signatures without downloading any model.

Run [scripts/print_model_mappings.py](scripts/print_model_mappings.py) to print supported embedder/reranker auto mappings from the installed package. Use this before writing model-selection guidance because package mappings can change.

## Capability Inventory

FlagEmbedding exposes these main user-facing capabilities:

| Capability | Primary route | Deep reference |
| --- | --- | --- |
| Embedding inference | `inference` | `sub-skills/inference/references/embedder-api.md` |
| Reranking inference | `inference` | `sub-skills/inference/references/reranker-api.md` |
| Model selection | root and `inference` | `references/model-overview.md` |
| Embedder fine-tuning | `finetuning` | `sub-skills/finetuning/references/training-workflows.md` |
| Reranker fine-tuning | `finetuning` | `sub-skills/finetuning/references/training-workflows.md` |
| Training data schemas | `finetuning` and `data-preparation` | `sub-skills/finetuning/references/data-formats.md` |
| Benchmark evaluation | `evaluation` | `sub-skills/evaluation/references/evaluation-workflows.md` |
| Custom dataset evaluation | `evaluation` | `sub-skills/evaluation/references/data-formats.md` |
| Hard-negative mining | `data-preparation` | `sub-skills/data-preparation/references/workflows.md` |
| Teacher-score distillation data | `data-preparation` | `sub-skills/data-preparation/references/workflows.md` |
| Length bucketing | `data-preparation` | `sub-skills/data-preparation/references/workflows.md` |

## Ground Rules

Prefer `FlagAutoModel.from_finetuned(...)` and `FlagAutoReranker.from_finetuned(...)` for known model names. For custom local checkpoints or model names absent from the auto mappings, set `model_class` explicitly.

Do not default to running model downloads, training, or benchmark downloads during diagnosis. Start with import/signature checks, data validation, and command construction. Make download/training commands explicit to the user.

When writing runnable examples, keep model cache paths generic, such as `./cache/model` or `$HF_HOME`, and keep output directories under a task-specific working directory.
