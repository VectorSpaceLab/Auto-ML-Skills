# Backend Reference

Use this for ONNX/OpenVINO loading and export helpers across `SentenceTransformer`, `CrossEncoder`, and `SparseEncoder`.

## Install Extras

```bash
pip install -U "sentence-transformers[onnx]"
pip install -U "sentence-transformers[onnx-gpu]"
pip install -U "sentence-transformers[openvino]"
```

`onnx-gpu` installs GPU-capable ONNX Runtime dependencies. OpenVINO uses `optimum-intel`.

## Loading Backends

```python
model = SentenceTransformer(model_id_or_path, backend="onnx")
model = CrossEncoder(model_id_or_path, backend="onnx")
model = SparseEncoder(model_id_or_path, backend="openvino")
```

Backend-specific options pass through `model_kwargs`, for example:

```python
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    backend="onnx",
    model_kwargs={"provider": "CPUExecutionProvider", "file_name": "onnx/model_O3.onnx"},
)
```

Common ONNX `model_kwargs`:

- `provider`: ONNX Runtime execution provider.
- `file_name`: specific ONNX file to load, such as an optimized or quantized file.
- `export`: whether to export if no ONNX file exists.

## Export Optimized ONNX

Verified signature:

```python
export_optimized_onnx_model(
    model,
    optimization_config: OptimizationConfig | Literal["O1", "O2", "O3", "O4"],
    model_name_or_path: str,
    push_to_hub: bool = False,
    create_pr: bool = False,
    file_suffix: str | None = None,
) -> None
```

Use with a model loaded with `backend="onnx"`.

`"O1"` through `"O4"` are Optimum optimization levels. Higher levels may be faster but can be more hardware/model sensitive.

## Export Dynamic Quantized ONNX

Verified signature:

```python
export_dynamic_quantized_onnx_model(
    model,
    quantization_config: QuantizationConfig | Literal["arm64", "avx2", "avx512", "avx512_vnni"],
    model_name_or_path: str,
    push_to_hub: bool = False,
    create_pr: bool = False,
    file_suffix: str | None = None,
) -> None
```

Dynamic quantization does not require a calibration dataset and is commonly used for CPU inference.

Choose a quantization config that matches deployment CPU capabilities.

## Export Static Quantized OpenVINO

Verified signature:

```python
export_static_quantized_openvino_model(
    model,
    quantization_config: OVQuantizationConfig | dict | None,
    model_name_or_path: str,
    dataset_name: str | None = None,
    dataset_config_name: str | None = None,
    dataset_split: str | None = None,
    column_name: str | None = None,
    push_to_hub: bool = False,
    create_pr: bool = False,
    file_suffix: str = "qint8_quantized",
) -> None
```

Static quantization can require calibration data. Use representative text or pair data for the model family.

## Backend Caveats

For SentenceTransformer ONNX exports, the exported ONNX component may be the Transformer component. If using ONNX outside the Sentence Transformers package, apply pooling and normalization yourself.

For SparseEncoder ONNX exports, external use may require SPLADE pooling outside ONNX. Within Sentence Transformers, the model wrapper handles the full pipeline.

For CrossEncoder ONNX exports used outside Sentence Transformers, apply the same activation function if you need identical post-activation scores.

## Save Exported Artifacts

If a backend export happens on first load, save it:

```python
model = SentenceTransformer("path/to/local-model", backend="onnx")
model.save_pretrained("path/to/local-model")
```

For Hub models, use `push_to_hub(..., create_pr=True)` or export helpers with `push_to_hub=True, create_pr=True` when contributing optimized files upstream.
