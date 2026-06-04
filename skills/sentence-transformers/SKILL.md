---
name: sentence-transformers
description: "Helps agents use Hugging Face Sentence Transformers for embeddings, retrieval, reranking, sparse encoders, training, evaluation, quantization, and backend export."
disable-model-invocation: true
---

# Sentence Transformers

Use this skill when a task involves the `sentence-transformers` Python package: dense or multimodal embeddings, semantic search, retrieve-and-rerank pipelines, sparse SPLADE-style embeddings, fine-tuning, evaluation, hard-negative mining, or model export for faster inference.

Sentence Transformers exposes Python APIs rather than a primary command-line interface. Pick the closest sub-skill first, then read only the linked reference files you need.

## Installation

Public package install:

```bash
pip install -U sentence-transformers
```

Common extras:

```bash
pip install -U "sentence-transformers[train]"
pip install -U "sentence-transformers[image]"
pip install -U "sentence-transformers[audio]"
pip install -U "sentence-transformers[video]"
pip install -U "sentence-transformers[onnx]"
pip install -U "sentence-transformers[onnx-gpu]"
pip install -U "sentence-transformers[openvino]"
```

For a public main-branch or editable install, use the project repository rather than a local checkout:

```bash
git clone https://github.com/huggingface/sentence-transformers.git
cd sentence-transformers
pip install -e ".[train]"
```

Minimum public requirements from package metadata: Python `>=3.10`, `torch>=1.11.0`, `transformers>=4.41.0,<6.0.0`, `huggingface-hub>=0.23.0`, `numpy`, `scikit-learn`, `scipy`, `typing_extensions`, and `tqdm`.

Minimal import check:

```bash
python - <<'PY'
import sentence_transformers
from sentence_transformers import SentenceTransformer, CrossEncoder, SparseEncoder
print(sentence_transformers.__version__)
print(SentenceTransformer, CrossEncoder, SparseEncoder)
PY
```

For a broader local diagnostic without downloading models, run [scripts/check_env.py](scripts/check_env.py).

## Choose A Sub-Skill

Use [sub-skills/sentence-transformer/SKILL.md](sub-skills/sentence-transformer/SKILL.md) for:

- `SentenceTransformer` dense embeddings for text, image, audio, video, or mixed-modal inputs.
- `encode`, `encode_query`, `encode_document`, embedding similarity, semantic search, clustering, paraphrase mining, and custom embedding modules.

Use [sub-skills/cross-encoder/SKILL.md](sub-skills/cross-encoder/SKILL.md) for:

- `CrossEncoder` pair scoring, passage ranking, reranking retrieved candidates, pair classification, and multimodal reranking.
- Understanding logits, activation functions, `predict`, `rank`, and second-stage retrieval workflows.

Use [sub-skills/sparse-encoder/SKILL.md](sub-skills/sparse-encoder/SKILL.md) for:

- `SparseEncoder` and SPLADE-style sparse embeddings.
- Sparse semantic search, sparse similarity, sparsity stats, decoding active terms, search-engine integration, and hybrid dense+sparse retrieval.

Use [sub-skills/training-and-evaluation/SKILL.md](sub-skills/training-and-evaluation/SKILL.md) for:

- Fine-tuning embedding, reranker, or sparse encoder models.
- Dataset formats, loss selection, trainers, training arguments, evaluators, hard-negative mining, distributed training, and model cards.

Use [sub-skills/optimization-and-deployment/SKILL.md](sub-skills/optimization-and-deployment/SKILL.md) for:

- ONNX and OpenVINO backends, dynamic/static quantization, embedding quantization, Matryoshka truncation, multi-device inference, and push/save deployment decisions.

## Shared References

Read [references/installation-and-capabilities.md](references/installation-and-capabilities.md) when you need install options, extras, model-family boundaries, public dependencies, or a capability map.

Read [references/troubleshooting.md](references/troubleshooting.md) when imports fail, model downloads fail, optional extras are missing, Hub access is blocked, training columns do not match a loss, a backend export fails, or scores look wrong.

## Default Workflow

1. Identify whether the user needs embeddings, reranking, sparse retrieval, training/evaluation, or deployment optimization.
2. Open the matching sub-skill `SKILL.md`.
3. Run `python scripts/check_env.py` if the environment is unknown.
4. Prefer `encode_query` and `encode_document` for retrieval models that define prompts; use plain `encode` for generic embedding tasks.
5. Prefer `CrossEncoder.rank` for reranking a query against documents; use `predict` for explicit input pairs or classification-style workflows.
6. For training, match the dataset column pattern to the loss before writing code; many failures are column/loss mismatches.
7. For export or quantization, install the relevant extra and verify backend support before loading a model with `backend="onnx"` or `backend="openvino"`.

## Important Defaults

Model loading from Hugging Face Hub may download weights unless `local_files_only=True` is set or a local model path is used. Private or gated models require a Hugging Face token.

Set `trust_remote_code=True` only when the model repository is trusted and the task requires custom model code.

Dense retrieval often benefits from `normalize_embeddings=True` plus dot product or cosine similarity. Cross Encoders are usually stronger but slower because each query-document pair is scored jointly.

MS MARCO Cross Encoder rerankers often return raw logits. If the user needs probabilities in `[0, 1]`, pass an explicit sigmoid activation at prediction time or model construction time, but do not change the ranking just to rescale scores.

Multimodal inputs require the matching package extra and a model whose `modalities` and `supports(...)` methods show the modality is available.

The `evals/` directory, if present in this generated skill, is a development artifact for quality review and is not part of the public runtime instructions.
