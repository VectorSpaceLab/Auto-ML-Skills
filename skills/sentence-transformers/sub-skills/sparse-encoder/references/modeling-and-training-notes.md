# Sparse Modeling And Training Notes

Use this for architectural context before implementing sparse custom models or training workflows. For full training scripts and loss selection, use the `training-and-evaluation` sub-skill.

## SPLADE Architecture

Typical SPLADE models use:

1. `Transformer` with `transformer_task="fill-mask"` to output masked-language-model logits.
2. `SpladePooling` to pool token logits into one vocabulary-sized sparse vector.

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder.modules import SpladePooling, Transformer

mlm = Transformer("google-bert/bert-base-uncased", transformer_task="fill-mask")
pooling = SpladePooling(pooling_strategy="max")
model = SparseEncoder(modules=[mlm, pooling], similarity_fn_name="dot")
```

Passing a fill-mask checkpoint to `SparseEncoder(...)` can create this default architecture automatically.

## Inference-Free SPLADE

Inference-free SPLADE usually routes queries through lightweight `SparseStaticEmbedding` while documents use a full SPLADE document encoder. This shifts compute to offline document indexing.

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder.modules import Router, SparseStaticEmbedding, SpladePooling, Transformer

doc_encoder = Transformer("google-bert/bert-base-uncased", transformer_task="fill-mask")
router = Router.for_query_document(
    query_modules=[SparseStaticEmbedding(tokenizer=doc_encoder.tokenizer, frozen=False)],
    document_modules=[doc_encoder, SpladePooling("max")],
)
model = SparseEncoder(modules=[router], similarity_fn_name="dot")
```

When training router models, set `router_mapping` in `SparseEncoderTrainingArguments` so dataset columns route correctly.

## Sparse Autoencoder / CSR

The package includes sparse autoencoder modules and CSR losses. Use `CSRLoss` when training `SparseAutoEncoder`-style models, because reconstruction and contrastive sparse representation objectives need to be combined.

## Sparse Loss Handoff

For SPLADE training, the main loss should be wrapped with `SpladeLoss` or `CachedSpladeLoss` to add sparsity regularization. `SparseMSELoss` is the notable standalone sparse loss for embedding-level distillation.

Common sparse main losses:

- `SparseMultipleNegativesRankingLoss` for `(anchor, positive)` pairs.
- `SparseMarginMSELoss` for teacher-margin distillation.
- `SparseDistillKLDivLoss` for teacher score distributions.
- `SparseCosineSimilarityLoss`, `SparseCoSENTLoss`, or `SparseAnglELoss` for pair-score datasets.

## Max Active Dimensions

`max_active_dims` can reduce sparse vector size by keeping only the strongest dimensions. Treat it as an effectiveness/latency/storage tradeoff and evaluate retrieval metrics after changing it.

## Interpretability Limits

Decoded tokens explain active dimensions, but sparse expansion terms are model outputs, not a perfect human rationale. Use them for debugging and inspection, not as legal or scientific explanations without validation.
