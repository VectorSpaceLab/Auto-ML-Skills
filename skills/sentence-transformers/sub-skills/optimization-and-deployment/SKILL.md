---
name: optimization-and-deployment
description: "Use for Sentence Transformers inference optimization, ONNX and OpenVINO backends, model export, dynamic/static quantization, embedding quantization, Matryoshka truncation, multi-device encoding, saving, and Hub deployment."
disable-model-invocation: true
---

# Optimization And Deployment

Use this sub-skill when the task is about making Sentence Transformers inference faster, smaller, cheaper, easier to serve, or easier to publish.

It covers PyTorch precision choices, ONNX/OpenVINO backends, backend export helpers, embedding quantization, Matryoshka truncation, multi-process embedding, and save/push deployment patterns across `SentenceTransformer`, `CrossEncoder`, and `SparseEncoder`.

## When To Use

Use this sub-skill when the user asks to:

- load models with `backend="onnx"` or `backend="openvino"`;
- export optimized ONNX, dynamic-quantized ONNX, or static-quantized OpenVINO models;
- quantize output embeddings to `int8`, `uint8`, `binary`, or `ubinary`;
- truncate dense embeddings for Matryoshka models;
- speed up inference with fp16/bf16, flash attention, batching, or multi-process encoding;
- save local model artifacts or push optimized variants to Hugging Face Hub;
- diagnose backend dependency availability or exported model selection.

Use model-family sub-skills for basic inference and `training-and-evaluation` for training quality.

## Read These Files

Read [references/backend-reference.md](references/backend-reference.md) for verified export helper signatures, install extras, backend loading behavior, and ONNX/OpenVINO caveats.

Read [references/embedding-optimization.md](references/embedding-optimization.md) for embedding quantization, precision options, Matryoshka truncation, normalization, indexing, and multi-process encoding.

Read [references/deployment-workflows.md](references/deployment-workflows.md) for save/push patterns, PR-based Hub export, local artifacts, offline loading, and serving considerations.

Read [references/troubleshooting.md](references/troubleshooting.md) when backend imports fail, export repeats, optimized files are not selected, output differs across backends, or quantization hurts recall.

Run [scripts/backend_availability_check.py](scripts/backend_availability_check.py) to inspect optional backend dependencies without loading models.

Run or adapt [scripts/embedding_quantization_demo.py](scripts/embedding_quantization_demo.py) to test output embedding quantization on a small local text list.

## Short Workflow

1. Identify bottleneck: model forward pass, vector storage, vector search, reranking latency, or deployment packaging.
2. For forward-pass latency, choose PyTorch precision, ONNX, or OpenVINO.
3. For vector storage/search cost, use output embedding quantization, Matryoshka truncation, sparse `max_active_dims`, or ANN indexes.
4. Install the relevant extra: `[onnx]`, `[onnx-gpu]`, or `[openvino]`.
5. Export/optimize once and save or push the artifact; do not re-export on every request.
6. Benchmark with realistic batch sizes and sequence lengths before declaring a backend faster.

## Backend Loading Examples

```python
from sentence_transformers import SentenceTransformer, CrossEncoder, SparseEncoder

dense = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", backend="onnx")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", backend="onnx")
sparse = SparseEncoder("naver/splade-v3", backend="openvino")
```

If a repo or directory already contains a backend file, the package can load it. Otherwise it may export on first load. Save or push the result for reuse.

## Export Helpers

```python
from sentence_transformers import export_dynamic_quantized_onnx_model, export_optimized_onnx_model

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", backend="onnx")
export_optimized_onnx_model(model, optimization_config="O3", model_name_or_path="local-model-dir")
export_dynamic_quantized_onnx_model(model, quantization_config="avx2", model_name_or_path="local-model-dir")
```

For OpenVINO static quantization:

```python
from sentence_transformers import export_static_quantized_openvino_model

export_static_quantized_openvino_model(
    model,
    quantization_config=None,
    model_name_or_path="local-model-dir",
    dataset_name="sentence-transformers/all-nli",
    dataset_split="train",
    column_name="sentence",
)
```

## Embedding Quantization

```python
embeddings = model.encode(texts, precision="int8")
```

or:

```python
from sentence_transformers import quantize_embeddings

quantized = quantize_embeddings(embeddings, precision="uint8", calibration_embeddings=calibration)
```

Evaluate recall after quantization. Binary quantization can be much smaller but is not appropriate for every model or metric.

## Matryoshka Truncation

For Matryoshka-compatible dense models:

```python
embeddings = model.encode(texts, truncate_dim=128)
```

or set `truncate_dim` in the constructor. Truncation changes dimensionality and requires compatible indexes.
