# Embedding Optimization

Use this when the bottleneck is vector size, search speed, model throughput, or multi-device embedding.

## PyTorch Precision

GPU inference can often use fp16 or bf16:

```python
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"torch_dtype": "float16"})
# or after load:
model.half()
```

```python
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"torch_dtype": "bfloat16"})
# or after load:
model.bfloat16()
```

For training, fp32 loading may be safer; mixed precision can be controlled by training arguments.

## Flash Attention

For compatible GPU stacks:

```python
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"attn_implementation": "flash_attention_2", "torch_dtype": "bfloat16"},
)
```

Flash attention support depends on installed kernels, hardware, PyTorch, Transformers, and architecture.

## Output Embedding Quantization

Direct encode-time quantization:

```python
embeddings = model.encode(texts, precision="int8")
```

Post-hoc quantization:

```python
from sentence_transformers import quantize_embeddings

quantized = quantize_embeddings(embeddings, precision="uint8", calibration_embeddings=calibration_embeddings)
```

Verified signature:

```python
quantize_embeddings(
    embeddings,
    precision: Literal["float32", "int8", "uint8", "binary", "ubinary"],
    ranges: np.ndarray | None = None,
    calibration_embeddings: np.ndarray | None = None,
) -> np.ndarray
```

Evaluate retrieval quality after quantization. Keep a representative calibration set for scalar quantization.

## Matryoshka Truncation

For models trained with Matryoshka losses, embeddings can be truncated:

```python
model = SentenceTransformer(model_id, truncate_dim=128)
embeddings = model.encode(texts)
```

or:

```python
embeddings = model.encode(texts, truncate_dim=128)
```

Indexes must be rebuilt when dimensionality changes.

## Dense Retrieval Storage

Common storage reductions:

- normalize embeddings and store `float16` where acceptable;
- quantize to `int8`/`uint8`;
- use binary embeddings for two-stage retrieval;
- truncate Matryoshka embeddings;
- use ANN/vector databases rather than exact matrix search for large corpora.

## Sparse Vector Optimization

Sparse Encoders support `max_active_dims`:

```python
embeddings = sparse_model.encode_document(corpus, max_active_dims=256)
```

This reduces active terms and index size. Validate recall and NDCG after changing it.

## Multi-Process Dense Encoding

```python
pool = model.start_multi_process_pool(["cuda:0", "cuda:1"])
try:
    embeddings = model.encode_multi_process(sentences, pool, batch_size=64)
finally:
    model.stop_multi_process_pool(pool)
```

Use for offline batch jobs. For online serving, persistent workers or a serving framework may be more appropriate.

## Batching

Batch size is a throughput/latency/memory tradeoff. Benchmark with production-like sequence lengths. Tiny batch benchmarks often understate backend optimizations.
