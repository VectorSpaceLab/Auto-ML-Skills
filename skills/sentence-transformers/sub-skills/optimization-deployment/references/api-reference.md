# Optimization And Deployment API Reference

Read this for verified backend/export and vector-compression signatures.

## Backend Loading

`SentenceTransformer`, `CrossEncoder`, and `SparseEncoder` constructors accept:

```python
backend: Literal["torch", "onnx", "openvino"] = "torch"
model_kwargs: dict | None = None
revision: str | None = None
local_files_only: bool = False
trust_remote_code: bool = False
```

Common ONNX `model_kwargs`:

- `provider`: ONNX Runtime provider such as `"CPUExecutionProvider"` or `"CUDAExecutionProvider"`.
- `file_name`: backend file such as `"onnx/model_O3.onnx"`.
- `export`: whether to export if no backend file exists.

## Export Helpers

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

Optimization levels:

- `O1`: basic general optimizations.
- `O2`: O1 plus extended optimizations and transformer fusions.
- `O3`: O2 plus GELU approximation.
- `O4`: O3 plus mixed precision; GPU-only.

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

Dynamic quantization is usually CPU-oriented and does not require calibration data.

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

Static OpenVINO quantization uses calibration data.

## Output Embedding Quantization

```python
quantize_embeddings(
    embeddings,
    precision: Literal["float32", "int8", "uint8", "binary", "ubinary"],
    ranges: np.ndarray | None = None,
    calibration_embeddings: np.ndarray | None = None,
) -> np.ndarray
```

`SentenceTransformer.encode` also accepts:

```python
precision: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32"
```

For int8, calibration embeddings or ranges improve quantization quality.

## Truncation

Constructor-level:

```python
SentenceTransformer(..., truncate_dim=128)
```

Per-call:

```python
model.encode(texts, truncate_dim=128)
```

Existing embeddings:

```python
truncate_embeddings(embeddings, truncate_dim)
```

## Save And Publish

```python
model.save_pretrained(
    path,
    model_name=None,
    create_model_card=True,
    train_datasets=None,
    safe_serialization=True,
)
```

```python
model.push_to_hub(
    repo_id,
    token=None,
    private=None,
    safe_serialization=True,
    commit_message=None,
    local_model_path=None,
    exist_ok=False,
    replace_model_card=False,
    train_datasets=None,
    revision=None,
    create_pr=False,
) -> str
```

The old `tags` parameter is removed. Append tags through `model.model_card_data.tags` before pushing.
