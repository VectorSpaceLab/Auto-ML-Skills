# Inference Troubleshooting

Read this for embedder and reranker runtime issues.

## Avoid Downloading During Basic Diagnosis

Run the bundled no-download script first:

```bash
python sub-skills/inference/scripts/smoke_inference_no_download.py
```

It checks imports, signatures, and auto mappings without instantiating Hugging Face models.

## Model Not Found In Mapping

For embedders:

```python
from FlagEmbedding import FlagAutoModel
model = FlagAutoModel.from_finetuned(
    "local-or-new-model",
    model_class="encoder-only-base",
    pooling_method="cls",
)
```

For rerankers:

```python
from FlagEmbedding import FlagAutoReranker
reranker = FlagAutoReranker.from_finetuned(
    "local-or-new-reranker",
    model_class="encoder-only-base",
)
```

Choose `model_class` from the root model overview. Do not guess between encoder-only and decoder-only; inspect the base architecture or model card.

## M3 Output Confusion

`BGEM3FlagModel.encode()` returns a dictionary when M3-specific modes are used. Dense vectors are under `dense_vecs`, lexical sparse weights under `lexical_weights`, and ColBERT vectors under `colbert_vecs`.

If downstream code expects a NumPy array, pass `return_dense=True, return_sparse=False, return_colbert_vecs=False` and read `result["dense_vecs"]`, or use an encoder-only model whose `encode()` returns vectors directly.

## Query Instructions Not Applied

For retrieval queries, use `encode_queries()`. It applies `query_instruction_for_retrieval` with `query_instruction_format`.

For corpus/passages, use `encode_corpus()`. Passages normally should not receive query instructions.

## Device Or Precision Failure

If `use_fp16=True` fails:

1. Retry with `use_fp16=False`.
2. Use a single device or CPU for diagnosis.
3. Reduce `batch_size`, `query_max_length`, `passage_max_length`, or `max_length`.
4. For decoder-only models on BF16-capable GPUs, consider `use_bf16=True`.

## Trust Remote Code

Some mapped non-BGE models set `trust_remote_code=True`. Ask before loading untrusted remote model code. For internal or audited models, pass `trust_remote_code=True` explicitly when required.

## Reranker Score Interpretation

Raw reranker scores can be negative or positive and should be compared within the same model and input setup. `normalize=True` applies sigmoid and returns values in `[0, 1]`, but that is not guaranteed to be calibrated across domains.
