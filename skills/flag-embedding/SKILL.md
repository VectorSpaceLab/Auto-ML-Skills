---
name: flag-embedding
description: "Use when working with FlagEmbedding or BGE models for embedding inference, reranking, fine-tuning, retrieval evaluation, model-class selection, data validation, or troubleshooting."
---

# FlagEmbedding Skill

Use this skill for the FlagEmbedding Python package, the BGE model family, and related embedding, reranking, fine-tuning, and evaluation workflows. It is a router: read only the sub-skill and references needed for the user's task.

## Install

For inference-only work:

```bash
python -m pip install -U FlagEmbedding
```

For fine-tuning or training-data preparation:

```bash
python -m pip install -U "FlagEmbedding[finetune]"
```

For development from a source checkout:

```bash
python -m pip install -e .
python -m pip install -e ".[finetune]"
```

Core runtime dependencies include `torch`, `transformers`, `datasets`, `accelerate`, `sentence_transformers`, `peft`, `ir-datasets`, `sentencepiece`, and `protobuf`. Fine-tuning extras add `deepspeed` and `flash-attn`, which are CUDA/compiler-sensitive and should be installed only when the training workflow needs them.

Verify a usable package environment with:

```bash
python - <<'PY'
import importlib.metadata as md
from FlagEmbedding import FlagAutoModel, FlagAutoReranker
print(md.version("FlagEmbedding"))
print(FlagAutoModel.__name__, FlagAutoReranker.__name__)
PY
```

Run `scripts/check_flagembedding_env.py` when you need a reusable import, version, and torch backend check that does not download models.

## Route Tasks

- Use `sub-skills/inference/SKILL.md` for embedding vectors, query/passages similarity, BGE-M3 dense/sparse/ColBERT modes, reranker scores, model-class selection, multi-device inference, and API troubleshooting.
- Use `sub-skills/finetuning/SKILL.md` for embedder or reranker training commands, JSONL train-data format, hard-negative mining, teacher-score generation, LoRA/deepspeed choices, and training-data validation.
- Use `sub-skills/evaluation/SKILL.md` for MTEB, BEIR, MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, or custom retrieval evaluation commands and dataset layout.

## Shared References

- Read `references/model-overview.md` to choose between BGE embedders, BGE-M3, LLM-based embedders, rerankers, and explicit `model_class` values.
- Read `references/troubleshooting.md` for install/import failures, model loading problems, device selection, optional dependency issues, and result-shape surprises.
- Read `references/evidence-and-coverage.md` when auditing what repository evidence informed this generated skill and how public capabilities map to bundled files.

## Shared Safe Scripts

- Run `scripts/check_flagembedding_env.py` after installation or dependency changes. It imports FlagEmbedding, reports package/API availability, and checks torch device visibility without model downloads.

Example:

```bash
python scripts/check_flagembedding_env.py --show-torch
```

## Public API Anchors

The package exports these public inference names from `FlagEmbedding`:

- Embedder loaders/classes: `FlagAutoModel`, `FlagModel`, `BGEM3FlagModel`, `FlagLLMModel`, `FlagICLModel`, `FlagPseudoMoEModel`, `EmbedderModelClass`.
- Reranker loaders/classes: `FlagAutoReranker`, `FlagReranker`, `FlagLLMReranker`, `LayerWiseFlagLLMReranker`, `LightWeightFlagLLMReranker`, `RerankerModelClass`.
- Base classes for custom implementations: `AbsEmbedder`, `AbsReranker`.

The auto loaders infer model class from known model names. For local checkpoints, custom checkpoints, or unknown Hugging Face model ids, pass an explicit `model_class` value described in `references/model-overview.md` and the inference API reference.

## Backend Guidance

For normal API inspection and CPU inference, CUDA is optional. For large BGE or decoder-only models, prefer an available GPU and pass `devices=["cuda:0"]` or a list of devices. If `devices` is omitted, FlagEmbedding chooses CUDA devices when torch sees them, then NPU/MUSA/MPS when available, otherwise CPU.

Use `use_fp16=True` for faster GPU inference on many models; use `use_fp16=False` on CPU or when half precision causes unsupported operation errors. Some decoder-only and training workflows use BF16 or LoRA-specific settings; route to the relevant sub-skill before changing precision.

## Safety Rules For Future Agents

- Do not run full model downloads, benchmark datasets, hard-negative mining, teacher-score generation, or training jobs unless the user asked for that side effect.
- Prefer local model paths when the user already has checkpoints.
- Validate JSONL training data and custom evaluation datasets before launching long jobs.
- Treat `trust_remote_code=True` as a deliberate user-facing risk decision; use it only when the selected model family requires it.
- Keep local machine paths, temporary inspection environments, and private cache locations out of user-facing generated instructions.
