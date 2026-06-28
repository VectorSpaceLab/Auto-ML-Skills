# Inference Troubleshooting

Use this when FlagEmbedding inference code imports successfully but model loading, device selection, output handling, or scoring behaves unexpectedly.

## Unknown Checkpoint Name In Auto Mapping

Symptom:

```text
ValueError: Model name '...' not found in the model mapping
```

Cause:

- `FlagAutoModel` and `FlagAutoReranker` map by checkpoint basename.
- Local fine-tuned checkpoints and renamed model directories often do not match built-in mapping keys.

Fix:

```python
model = FlagAutoModel.from_finetuned(
    "./local-embedder",
    model_class="encoder-only-base",
    pooling_method="cls",
    use_fp16=False,
    devices="cpu",
)

reranker = FlagAutoReranker.from_finetuned(
    "./local-reranker",
    model_class="encoder-only-base",
    use_fp16=False,
    devices="cpu",
)
```

Choose the explicit `model_class` that matches the base architecture used for fine-tuning. For `checkpoint-...` directories, the auto loader checks the parent directory name; renaming the parent to a mapped model basename can also work, but explicit `model_class` is clearer in reusable code.

## Model Download, Network, Cache, Or Token Failures

Symptoms:

- Hugging Face connection timeouts.
- Authentication errors for gated/private models.
- Cache corruption or missing model files.
- Offline machines attempting downloads unexpectedly.

Fixes:

- Use a local checkpoint directory when offline.
- Pre-download the model with the same environment that will run inference.
- Set standard Hugging Face environment variables outside generated public code, such as `HF_HOME`, `TRANSFORMERS_CACHE`, `HF_TOKEN`, or a mirror endpoint, according to the deployment policy.
- For private/gated models, authenticate before loading or pass a supported Hugging Face token argument through `**kwargs` if the installed Transformers version accepts it.
- If cache corruption is suspected, clear only the affected model cache entry rather than all caches.
- Keep snippet generators and environment diagnostics no-download by default; do not instantiate `from_finetuned()` in health checks unless model download is intentional.

## Unexpected Device Selection

Symptoms:

- Code unexpectedly uses all GPUs.
- Integer device `0` selects CUDA when CPU was intended.
- Multi-process workers start when encoding a list.
- MPS/NPU/MUSA is selected on a machine with those backends.

Cause:

- `devices=None` auto-selects available CUDA, NPU, MUSA, MPS, then CPU.
- Integer devices become CUDA or MUSA device strings.
- Multiple target devices trigger multi-process behavior for list inputs.

Fixes:

- Force CPU with `devices="cpu"`.
- Force one accelerator with a string such as `devices="cuda:0"`.
- Use string lists, not integer lists, when the backend must be explicit.
- Reduce to one device when multiprocessing conflicts with an application server or notebook.
- Call `stop_self_pool()` when disposing multi-device models in long-running processes.

## FP16 Or BF16 Hardware Problems

Symptoms:

- CPU errors involving half precision operations.
- CUDA/MPS precision errors.
- NaN scores or degraded ranking after enabling half precision.
- Warnings that layerwise/lightweight rerankers force half precision.

Fixes:

- CPU-safe baseline: `use_fp16=False`, `use_bf16=False`, `devices="cpu"`.
- Enable `use_fp16=True` only on hardware known to support it for the selected model.
- Enable `use_bf16=True` only for compatible accelerators.
- If quality changes matter, compare retrieval/reranking outputs between FP32 and half precision on a validation set.
- For layerwise/lightweight rerankers, note that model constraints may force a half precision mode even if both half flags are false.

## BGE-M3 Dict Output Mismatch

Symptoms:

```text
AttributeError: 'dict' object has no attribute 'shape'
TypeError: unsupported operand type(s) for @: 'dict' and 'dict'
KeyError: 'dense_vecs'
```

Cause:

- `BGEM3FlagModel` returns dictionaries for dense/sparse/ColBERT outputs, not a plain embedding matrix.
- Keys depend on flags such as `return_dense`, `return_sparse`, and `return_colbert_vecs`.

Fix:

```python
outputs = model.encode(
    texts,
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)
dense = outputs["dense_vecs"]
lexical = outputs["lexical_weights"]
```

Use `outputs["dense_vecs"]` for dense vector indexes, `outputs["lexical_weights"]` for sparse lexical scoring, and `outputs["colbert_vecs"]` only for downstream code designed for multi-vector late interaction.

## Sparse Or ColBERT Scores Look Wrong

Causes:

- Query and passage outputs were encoded with different return flags.
- The code used raw token ids instead of converted lexical weights.
- ColBERT vectors were disabled by `return_colbert_vecs=False`.
- Dense-only downstream code silently ignored sparse or ColBERT information.

Fixes:

- Use matching flags for query and corpus encoding.
- For sparse matching, call `compute_lexical_matching_score(query_lexical, passage_lexical)`.
- For ColBERT workflows, set `return_colbert_vecs=True` and verify downstream scoring supports token-level vectors.
- For hybrid scoring, document weights and keep the selected modes explicit.

## Reranker Score Normalization Confusion

Symptoms:

- Scores differ from examples by being in `[0, 1]` instead of raw logits.
- Thresholds do not transfer between raw and normalized scores.

Cause:

- `compute_score(..., normalize=True)` applies sigmoid normalization.
- `normalize=False` returns raw model scores.

Fixes:

- Use raw scores for ranking unless the downstream application expects normalized values.
- Use normalized scores for display or coarse thresholding.
- Do not mix raw and normalized scores in one ranking list.

## Layerwise And Lightweight Reranker Kwarg Errors

Symptoms:

- `cutoff_layers` is ignored or rejected.
- `compress_ratio` or `compress_layers` causes unexpected keyword errors.
- Quality changes substantially when selecting lower layers.

Fixes:

- Use `LayerWiseFlagLLMReranker` or `model_class="decoder-only-layerwise"` when passing `cutoff_layers`.
- Use `LightWeightFlagLLMReranker` or `model_class="decoder-only-lightweight"` when passing `compress_ratio` and `compress_layers`.
- Keep layer choices explicit in code, for example `cutoff_layers=[28]`.
- Validate ranking quality for chosen layer/compression settings; lower layers and compression are efficiency trade-offs.

## Instruction Formatting Errors

Symptoms:

- `IndexError` or formatting exceptions from instruction format strings.
- Retrieval quality drops because instructions were applied to passages unintentionally.
- Literal `\n` appears in prompts where a newline was intended.

Fixes:

- Use exactly two `{}` replacement slots: one for the instruction and one for the text.
- Use `encode_queries()` for query instructions and `encode_corpus()` for passages.
- Pass passage instructions separately only when the model or task requires them.
- Literal `"\\n"` in the format is converted to a newline by base helper methods.

## Max Length And Memory Errors

Symptoms:

- CUDA out-of-memory errors.
- CPU inference stalls or swaps.
- Long passages truncate away relevant evidence.

Fixes:

- Lower `batch_size` first.
- Lower `query_max_length` for short queries.
- Tune `passage_max_length` or `max_length` based on passage length and model context.
- Use a smaller model or CPU-safe batch when deployment hardware is constrained.
- For BGE-M3 ColBERT, disable `return_colbert_vecs` unless multi-vector retrieval is required.

## Import Or Backend Diagnostics

Run the bundled no-download diagnostic:

```bash
python scripts/check_inference_env.py --show-mappings
```

It checks imports, package version metadata, torch backend availability, device resolution helpers, and mapping keys without loading or downloading model checkpoints.
