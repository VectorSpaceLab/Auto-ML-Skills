# Optimization And Deployment Troubleshooting

## Backend Import Fails

Run:

```bash
python scripts/backend_availability_check.py
```

Install the needed extra:

```bash
pip install -U "sentence-transformers[onnx]"
pip install -U "sentence-transformers[onnx-gpu]"
pip install -U "sentence-transformers[openvino]"
```

## Model Re-Exports Every Run

Save the exported model directory or push the generated artifact. If loading from Hub, specify the optimized file by name after it exists.

## Optimized File Is Not Used

Pass `model_kwargs={"file_name": "onnx/model_O3.onnx"}` or the relevant backend file name. Confirm the file exists in the local directory or Hub revision.

## ONNX Output Differs From PyTorch

Small numerical differences are expected. For SentenceTransformer exports used outside the package, ensure pooling and normalization are applied exactly as in the original model. For CrossEncoder exports used outside the package, apply the same activation function.

## Quantization Hurts Retrieval

Evaluate recall/NDCG before and after quantization. Try:

- representative calibration embeddings;
- `uint8` before `binary`;
- reranking top candidates from quantized search with float embeddings or a Cross Encoder;
- Matryoshka truncation instead of aggressive quantization if the model supports it.

## Matryoshka Truncation Breaks The Index

Changing `truncate_dim` changes embedding dimensionality. Rebuild vector indexes and update schema metadata.

## Backend Is Slower

Benchmark realistic batch size and sequence length. For tiny batches, export overhead or runtime overhead can dominate. ONNX/OpenVINO speedups are workload and hardware dependent.

## GPU Precision Errors

fp16/bf16 support depends on hardware and model architecture. Fall back to fp32 if you see NaNs, unsupported operation errors, or quality regressions.
