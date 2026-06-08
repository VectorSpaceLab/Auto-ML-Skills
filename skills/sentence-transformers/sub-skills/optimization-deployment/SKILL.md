---
name: optimization-deployment
description: "Optimize, export, quantize, deploy, save, publish, and migrate sentence-transformers models with PyTorch, ONNX, OpenVINO, fp16/bf16, embedding quantization, Matryoshka truncation, and backend troubleshooting."
---

# Optimization And Deployment

Use this sub-skill for inference speed, memory reduction, export, quantization, model saving/loading, Hub publishing, offline deployment, and migration/deprecation updates.

## Required Reading

- `references/api-reference.md`: verified backend/export/quantization signatures.
- `references/workflows.md`: PyTorch speedups, ONNX/OpenVINO recipes, output quantization, Matryoshka, offline and Hub deployment.
- `scripts/embedding_optimization_smoke.py`: safe local smoke script for output quantization/truncation without model export.

Also read root `../../references/troubleshooting.md` for backend-specific failures.

## Choose The Optimization

| Goal | Technique |
| --- | --- |
| GPU inference speed | larger batches, fp16/bf16, flash attention where compatible |
| CPU inference speed | ONNX dynamic quantization, OpenVINO, smaller/static embedding models |
| lower vector storage/search cost | output embedding quantization (`int8`, `uint8`, `binary`, `ubinary`) |
| variable embedding dimension | Matryoshka truncation with `truncate_dim` or `truncate_embeddings` |
| reusable optimized model | save ONNX/OpenVINO artifacts with `save_pretrained` or export helpers |
| no network in production | pre-download and save locally; load with `local_files_only=True` |

Do not combine optimizations blindly. Measure task quality and latency after each change.

## PyTorch Speed Defaults

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"torch_dtype": "float16"},
)
embeddings = model.encode(texts, batch_size=128)
```

Use `bfloat16` on hardware that supports it well. For flash attention, set `model_kwargs={"attn_implementation": "flash_attention_2", "torch_dtype": "bfloat16"}` only when the dependency/model combination supports it.

## ONNX And OpenVINO

Install the matching extra:

```bash
pip install -U "sentence-transformers[onnx]"       # CPU
pip install -U "sentence-transformers[onnx-gpu]"   # GPU
pip install -U "sentence-transformers[openvino]"
```

Load with a backend:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", backend="onnx")
embeddings = model.encode(["This is an example sentence"])
model.save_pretrained("models/all-MiniLM-L6-v2-onnx")
```

If a repository already has compatible backend files, Sentence Transformers uses them; otherwise it can export on first load. Save the result so production does not re-export every run.

## Output Embedding Quantization

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(texts, precision="int8")
```

Or quantize existing embeddings:

```python
from sentence_transformers.util.quantization import quantize_embeddings

embeddings_int8 = quantize_embeddings(embeddings_float32, precision="int8", calibration_embeddings=calibration)
```

Validate recall/quality after quantization.

## Matryoshka Truncation

For Matryoshka-trained models:

```python
model = SentenceTransformer("tomaarsen/mpnet-base-nli-matryoshka", truncate_dim=128)
embeddings = model.encode(texts)
```

Or:

```python
from sentence_transformers.util import truncate_embeddings
small = truncate_embeddings(embeddings, 128)
```

Only assume graceful degradation for models trained for truncation.

## Deployment And Publishing

Save locally:

```python
model.save_pretrained("models/my-model")
```

Load offline:

```python
model = SentenceTransformer("models/my-model", local_files_only=True)
```

Push to Hub:

```python
model.push_to_hub("org-or-user/model-name", private=False, create_pr=False)
```

For generated code, avoid hardcoding tokens. Use environment authentication or pass a token from user-controlled config.
