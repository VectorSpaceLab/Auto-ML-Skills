# Troubleshooting

Read this for cross-cutting failures that apply across the package. Sub-skills include more specific troubleshooting files for dense embeddings, Cross Encoders, Sparse Encoders, training, and backend export.

## Import Or Install Problems

If `import sentence_transformers` fails, check the active Python first:

```bash
python -m pip show sentence-transformers
python - <<'PY'
import sys
print(sys.executable)
print(sys.version)
PY
```

Use Python `>=3.10`. If the package imports but multimodal, training, ONNX, or OpenVINO imports fail, install the matching extra.

If importing triggers a long startup delay, isolate whether the delay is from `torch`, `transformers`, GPU discovery, or a broken site package:

```bash
python - <<'PY'
import importlib, time
for name in ["torch", "transformers", "sentence_transformers"]:
    start = time.time()
    importlib.import_module(name)
    print(name, round(time.time() - start, 2), "s")
PY
```

## Model Download And Hub Access

Hub downloads require network access unless the model is cached or a local path is used. Use `local_files_only=True` for offline runs.

Private or gated models require a token. Pass `token=...` to model constructors or configure Hugging Face Hub authentication outside the script.

Only pass `trust_remote_code=True` for model repositories the user trusts. It allows model code from the repository to execute locally.

## Optional Extras Missing

Symptoms:

- Image/audio/video inputs fail even though text inputs work.
- `backend="onnx"` or `backend="openvino"` fails at load time.
- Trainer imports complain about `datasets` or `accelerate`.

Fix by installing the relevant extra:

```bash
pip install -U "sentence-transformers[image]"
pip install -U "sentence-transformers[train]"
pip install -U "sentence-transformers[onnx]"
pip install -U "sentence-transformers[openvino]"
```

## Scores Look Wrong

Dense embedding similarities depend on both the similarity function and normalization. If you plan to use dot product as cosine-like retrieval, encode with `normalize_embeddings=True`.

For retrieval models with prompts, use `encode_query` for queries and `encode_document` for documents. Plain `encode` may skip query/document-specific prompts.

MS MARCO Cross Encoder rerankers commonly return logits rather than probabilities. This is expected for ranking. If probabilities are needed, use a sigmoid activation, but do not compare sigmoid scores against raw logits.

Sparse Encoder dot-product scores are not bounded to `[0, 1]`; large positive values can be normal.

## Out Of Memory Or Slow Runs

Reduce `batch_size`, use smaller models, use `truncate_dim` for Matryoshka-compatible dense models, use `max_active_dims` for sparse embeddings, or switch to ONNX/OpenVINO when supported.

For large dense corpora, embed documents once, store the vectors, and use chunked `semantic_search` or an ANN index. Do not call a Cross Encoder over the whole corpus.

For multi-GPU or multi-process embedding, use the dense sub-skill and the optimization sub-skill together.

## Training Column Mismatch

Trainer losses infer columns from the `datasets.Dataset`. Common formats include:

- `(anchor, positive)` with no labels for in-batch-negative losses.
- `(anchor, positive, negative)` for triplet-style or ranking losses.
- `(text_a, text_b, score)` for similarity regression.
- `(query, document, label)` for Cross Encoder binary scoring.
- `(query, documents, scores)` for listwise reranker losses.

If a loss fails at collate time, inspect dataset column names and compare them with [sub-skills/training-and-evaluation/references/data-formats.md](../sub-skills/training-and-evaluation/references/data-formats.md).

## Backend Export Problems

ONNX and OpenVINO export require the model family to be supported by the backend dependencies. Install the relevant extra, verify package availability with [../scripts/check_env.py](../scripts/check_env.py), then use [sub-skills/optimization-and-deployment/scripts/backend_availability_check.py](../sub-skills/optimization-and-deployment/scripts/backend_availability_check.py).

If an exported model is slower than PyTorch for tiny batches, benchmark realistic batch sizes. Optimized backends usually matter most in repeated inference or larger deployment workloads.

## Sparse Encoder Specific Pitfalls

Sparse tensors may be large in dimensionality even when most values are zero. Keep them sparse where possible and avoid unnecessary dense conversion.

For SPLADE training, wrap the main loss with `SpladeLoss` or `CachedSpladeLoss` so sparsity regularization is applied. `SparseMSELoss` is the notable standalone sparse loss for embedding-level distillation.
