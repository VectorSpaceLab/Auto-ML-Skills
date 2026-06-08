---
name: sentence-transformers
description: "Use sentence-transformers for embeddings, semantic search, reranking, sparse retrieval, model training/evaluation, ONNX/OpenVINO export, quantization, migration, and troubleshooting across SentenceTransformer, CrossEncoder, and SparseEncoder workflows."
---

# Sentence Transformers

Use this skill when a user wants to build with the `sentence-transformers` Python package: dense embeddings, semantic search, retrieve-and-rerank, CrossEncoder scoring, SparseEncoder/SPLADE retrieval, training, evaluation, model export, optimization, or migration help.

Keep this file as the router. Load the nearest sub-skill and references for implementation details before writing code.

## Install And Verify

Public install requirements: Python 3.10+, PyTorch 1.11+, and Transformers 4.41+.

```bash
pip install -U sentence-transformers
python - <<'PY'
import sentence_transformers
from sentence_transformers import SentenceTransformer, CrossEncoder, SparseEncoder
print(sentence_transformers.__version__)
print(SentenceTransformer.__name__, CrossEncoder.__name__, SparseEncoder.__name__)
PY
```

Extras:

```bash
pip install -U "sentence-transformers[image]"       # image-capable models
pip install -U "sentence-transformers[audio]"       # audio-capable models
pip install -U "sentence-transformers[video]"       # video-capable models
pip install -U "sentence-transformers[train]"       # trainers, datasets, accelerate
pip install -U "sentence-transformers[onnx]"        # ONNX CPU
pip install -U "sentence-transformers[onnx-gpu]"    # ONNX GPU
pip install -U "sentence-transformers[openvino]"    # OpenVINO
```

For conda, the base package is available from conda-forge:

```bash
conda install -c conda-forge sentence-transformers
```

Conda does not provide pip extras; install extras with pip when needed.

## Route By Task

- Dense embeddings, semantic textual similarity, clustering, paraphrase mining, dense semantic search, multimodal embeddings, query/document prompts: read `sub-skills/dense-embeddings/SKILL.md`.
- CrossEncoder pair scoring, reranking, retrieve-and-rerank, pair classification, MS MARCO logits, multimodal rerankers: read `sub-skills/reranking/SKILL.md`.
- SparseEncoder/SPLADE embeddings, sparse semantic search, token-level interpretability, Qdrant/OpenSearch sparse integration, hybrid retrieval: read `sub-skills/sparse-retrieval/SKILL.md`.
- Training, fine-tuning, loss selection, evaluator selection, hard-negative mining, dataset shapes, trainer arguments: read `sub-skills/training-evaluation/SKILL.md`. If the repo-local `train-sentence-transformers` skill is installed, use it for full production training templates.
- ONNX, OpenVINO, backend selection, fp16/bf16 inference, output embedding quantization, Matryoshka truncation, Hub publishing, migration and deprecations: read `sub-skills/optimization-deployment/SKILL.md`.

## Cross-Cutting References

- `references/package-overview.md`: package architecture, installation extras, model classes, supported inputs, and import-path guidance.
- `references/troubleshooting.md`: install, import, download, backend, scoring, and migration symptoms.
- `scripts/check_sentence_transformers_env.py`: safe environment/import/backend diagnostic. Run it before deeper debugging or after installing extras.

## Core Model Choice

| User intent | Class | Typical output | Notes |
| --- | --- | --- | --- |
| embeddings, vector search, clustering, STS, paraphrase mining | `SentenceTransformer` | dense vectors | Efficient first-stage retrieval and similarity. |
| reranking, pair scoring, pair classification | `CrossEncoder` | one score or class logits per pair | More accurate per pair but slower; use on candidates. |
| learned sparse retrieval, SPLADE, token interpretability | `SparseEncoder` | sparse vectors over vocabulary dimensions | Good for sparse search engines and hybrid retrieval. |

Use `encode_query` and `encode_document` for retrieval models with query/document prompts or Router modules. Use plain `encode` for symmetric similarity, clustering, classification features, or models without retrieval-specific prompts.

## Safe Minimal Examples

Dense embeddings:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = ["The weather is lovely today.", "It is sunny outside.", "He drove to the stadium."]
embeddings = model.encode(texts)
scores = model.similarity(embeddings, embeddings)
```

Reranking:

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
query = "How many people live in Berlin?"
passages = ["Berlin had a population of 3,520,031.", "Berlin is known for museums."]
ranks = model.rank(query, passages, return_documents=True)
```

Sparse retrieval:

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.util import semantic_search

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
corpus_embeddings = model.encode_document(["Mars rovers explore Mars."], convert_to_tensor=True)
query_embeddings = model.encode_query(["What explores Mars?"], convert_to_tensor=True)
hits = semantic_search(query_embeddings, corpus_embeddings, score_function=model.similarity)
```

## Decision Points

- Retrieval with short queries and longer documents is asymmetric: prefer retrieval-tuned models and `encode_query`/`encode_document`.
- Similar sentence/question matching is symmetric: a general embedding model and `encode` are often enough.
- Large corpora need an index. `util.semantic_search` is exact and practical up to roughly 1M entries; use FAISS, hnswlib, Annoy, Elasticsearch, OpenSearch, Qdrant, or another vector database beyond that.
- CrossEncoders should rerank top-k candidates, not score an entire large corpus pair-by-pair.
- MS MARCO CrossEncoder models often return logits; ranking is unaffected, but load with `activation_fn=torch.nn.Sigmoid()` when calibrated 0-1 scores are required.
- Multimodal models require matching extras such as `[image]`, `[audio]`, or `[video]`; inspect `model.modalities` and `model.supports(...)`.

## Evidence Base

This generated skill was built from package metadata, docs, examples, tests, source modules, the existing training skill, and live installed-package inspection of `sentence-transformers` 5.6.0.dev0 APIs. Generated runtime guidance avoids machine-specific setup details.
