# Inference Troubleshooting

Read this when an embedding or reranking workflow fails after the package imports.

## Auto Mapping Error

Symptom:

```text
Model name '...' not found in the model mapping
```

Fix:

- For encoder-only BGE checkpoints, pass `model_class="encoder-only-base"` and a known `pooling_method` such as `cls`.
- For BGE-M3 checkpoints, pass `model_class="encoder-only-m3"`.
- For decoder-only embedding checkpoints, use `decoder-only-base`, `decoder-only-icl`, or `decoder-only-pseudo_moe`.
- For rerankers, use `encoder-only-base`, `decoder-only-base`, `decoder-only-layerwise`, or `decoder-only-lightweight`.

## Unexpected Device Use

If `devices` is omitted, FlagEmbedding can use every visible CUDA device. Pass explicit devices to avoid surprising resource use:

```python
devices=["cuda:0"]
devices="cpu"
```

For CPU inference, pass `use_fp16=False`.

## Query Instructions Not Applied

Use `encode_queries()` instead of `encode()` when query instructions should be applied. Pass `query_instruction_for_retrieval` and `query_instruction_format` at model construction.

For passages, use `encode_corpus()` unless the task explicitly requires passage instructions.

## Result Type Confusion

Normal embedders return vectors directly. BGE-M3 returns a dictionary when using sparse or ColBERT modes. Rerankers return scores, not vectors.

If downstream code expects numpy arrays, keep `convert_to_numpy=True`. If it expects torch tensors, pass `convert_to_numpy=False` where supported and handle device placement.

## Slow Or Memory-Heavy Runs

- Reduce `batch_size`.
- Lower `query_max_length`, `passage_max_length`, or `max_length`.
- Use a smaller model.
- Use one explicit GPU before trying multi-device multiprocessing.
- Disable ColBERT vectors unless needed.
- For reranking many passages, retrieve top-k with embeddings first, then rerank only the shortlist.

## Optional Remote Code

Some mapped models set or require `trust_remote_code=True`. Only enable it when the model family requires custom code and the user accepts the risk.
