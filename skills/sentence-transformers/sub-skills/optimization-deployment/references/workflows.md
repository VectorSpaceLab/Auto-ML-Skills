# Optimization And Deployment Workflows

Read this before changing inference backend, vector precision, or deployment packaging.

## Baseline First

Always capture a baseline:

```python
import time
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_id)
start = time.perf_counter()
embeddings = model.encode(texts, batch_size=32)
elapsed = time.perf_counter() - start
print(embeddings.shape, elapsed)
```

Then compare latency, memory, and task metric after each optimization.

## GPU PyTorch Optimization

```python
model = SentenceTransformer(model_id, model_kwargs={"torch_dtype": "bfloat16"})
embeddings = model.encode(texts, batch_size=128)
```

Use `float16` or `bfloat16` only on suitable hardware. If using flash attention:

```python
model = SentenceTransformer(
    model_id,
    model_kwargs={"attn_implementation": "flash_attention_2", "torch_dtype": "bfloat16"},
)
```

If variable-length unpadding causes model-specific issues, inspect and adjust the first transformer module's `unpad_inputs` setting.

## ONNX Export And Reuse

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_id, backend="onnx")
model.save_pretrained("models/model-onnx")

model = SentenceTransformer("models/model-onnx", backend="onnx", local_files_only=True)
```

When loading a specific optimized file:

```python
model = SentenceTransformer(
    model_id,
    backend="onnx",
    model_kwargs={"file_name": "onnx/model_O3.onnx"},
)
```

## Optimize ONNX Once

```python
from sentence_transformers import SentenceTransformer, export_optimized_onnx_model

model = SentenceTransformer(model_id, backend="onnx")
export_optimized_onnx_model(model, optimization_config="O3", model_name_or_path=output_path)
```

For Hub models without write access, use `push_to_hub=True, create_pr=True`.

## Dynamic ONNX Quantization

```python
from sentence_transformers import SentenceTransformer, export_dynamic_quantized_onnx_model

model = SentenceTransformer(model_id, backend="onnx")
export_dynamic_quantized_onnx_model(model, quantization_config="avx512_vnni", model_name_or_path=output_path)
```

Choose `avx2`, `avx512`, or `avx512_vnni` based on deployment CPU capabilities. Validate performance on the actual host.

## OpenVINO

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_id, backend="openvino")
embeddings = model.encode(texts)
model.save_pretrained("models/model-openvino")
```

For static quantization, provide calibration data through `export_static_quantized_openvino_model`.

## Output Vector Quantization

Use when storage/search cost is the bottleneck.

```python
embeddings = model.encode(texts, precision="int8")
```

For existing vectors:

```python
from sentence_transformers.util.quantization import quantize_embeddings

calibration = model.encode(calibration_texts)
embeddings_int8 = quantize_embeddings(embeddings, precision="int8", calibration_embeddings=calibration)
```

Binary and unsigned-binary vectors are much smaller but require compatible search logic and metric validation.

## Matryoshka

Use only with Matryoshka-trained models:

```python
model = SentenceTransformer(model_id, truncate_dim=128)
embeddings = model.encode(texts)
```

Evaluate multiple dimensions, for example 64, 128, 256, and full dimension, against the user's retrieval metric.

## Offline Deployment

1. Download and save the model in a connected environment.
2. Copy the saved directory to deployment.
3. Load with `local_files_only=True`.
4. Pin package versions and backend files.

```python
model = SentenceTransformer("models/my-saved-model", local_files_only=True)
```

Avoid relying on implicit Hub downloads in production startup paths.

## Hub Publishing

```python
model.model_card_data.tags.append("my-domain")
url = model.push_to_hub("org/model-name", private=True)
```

Use `create_pr=True` when contributing optimized files to a model repository without direct write access.

## Migration Review Checklist

- Replace old internal imports with model-type-specific packages.
- Use `processor_kwargs`, not `tokenizer_kwargs`.
- Use trainer `processing_class`, not `tokenizer`.
- Use `get_embedding_dimension`, not `get_sentence_embedding_dimension`.
- Do not pass removed `tags=` to `push_to_hub`.
- Update custom CrossEncoder losses for `model(... )["scores"]` and optional `prompt`/`task`.
