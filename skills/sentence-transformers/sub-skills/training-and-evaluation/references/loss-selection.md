# Loss Selection

Choose losses from dataset format, labels, and model family. This file summarizes common choices; inspect loss docstrings or source for rare edge cases.

## Dense SentenceTransformer Losses

| Data | Labels | Common losses |
| --- | --- | --- |
| `anchor, positive` | none | `MultipleNegativesRankingLoss`, `CachedMultipleNegativesRankingLoss`, `GISTEmbedLoss`, `CachedGISTEmbedLoss`, `MegaBatchMarginLoss` |
| `anchor, positive, negative` | none | `MultipleNegativesRankingLoss`, `CachedMultipleNegativesRankingLoss`, `TripletLoss`, `GISTEmbedLoss` |
| `sentence1, sentence2` | float score | `CoSENTLoss`, `AnglELoss`, `CosineSimilarityLoss` |
| `sentence1, sentence2` | class | `SoftmaxLoss` |
| `anchor, positive/negative` | 1/0 label | `ContrastiveLoss`, `OnlineContrastiveLoss` |
| single input | class | `BatchAllTripletLoss`, `BatchHardTripletLoss`, `BatchSemiHardTripletLoss`, `BatchHardSoftMarginTripletLoss` |
| input(s) | teacher embeddings | `MSELoss`, `EmbedDistillLoss` |
| query/document pairs or triplets | teacher scores/margins | `MarginMSELoss`, `DistillKLDivLoss` |

Modifiers:

- `MatryoshkaLoss` for truncatable embeddings.
- `Matryoshka2dLoss` for layer and dimension truncation.
- `AdaptiveLayerLoss` for layer-dropping robustness.
- `GlobalOrthogonalRegularizationLoss` for embedding-space regularization.

## Cross Encoder Losses

| Data | Labels | Output labels | Common losses |
| --- | --- | --- | --- |
| pair | 0/1 or float relevance | 1 | `BinaryCrossEntropyLoss`, `MSELoss` |
| pair | class id | N | `CrossEntropyLoss` |
| anchor, positive | none | 1 | `MultipleNegativesRankingLoss`, `CachedMultipleNegativesRankingLoss` |
| query, positive, negative | teacher margin | 1 | `MarginMSELoss` |
| query, documents list | score list | 1 | `LambdaLoss`, `PListMLELoss`, `ListNetLoss`, `RankNetLoss`, `ListMLELoss`, `ADRMSELoss` |

Common choices:

- Use `BinaryCrossEntropyLoss` for binary query-document relevance labels.
- Use `LambdaLoss` with labeled-list hard negatives for learning-to-rank tasks.
- Use `CrossEntropyLoss` only when the model has multiple output labels.

## Sparse Encoder Losses

Sparse losses mirror dense loss formats but need sparsity-aware wrappers for SPLADE:

| Data | Labels | Common main losses |
| --- | --- | --- |
| `anchor, positive` | none | `SparseMultipleNegativesRankingLoss` |
| `anchor, positive, negative` | none | `SparseMultipleNegativesRankingLoss`, `SparseTripletLoss` |
| `sentence1, sentence2` | float score | `SparseCoSENTLoss`, `SparseAnglELoss`, `SparseCosineSimilarityLoss` |
| teacher embeddings | sparse teacher embeddings | `SparseMSELoss` |
| teacher scores/margins | score/margin labels | `SparseMarginMSELoss`, `SparseDistillKLDivLoss` |

Wrappers and regularizers:

- `SpladeLoss`: wraps a main sparse loss and adds FLOPS/sparsity regularization.
- `CachedSpladeLoss`: GradCache variant for larger effective batches.
- `CSRLoss`: use with `SparseAutoEncoder`/CSR workflows.
- `FlopsLoss`: common sparse regularizer inside SPLADE losses.

## Hard Negative Mining Link

If the dataset only has positive pairs but the desired loss needs negatives, use `mine_hard_negatives` to create triplets, n-tuples, labeled pairs, or labeled lists.

## Quality Guidance

Use an evaluator that measures the target behavior. A low training loss does not prove retrieval quality, reranking quality, calibration, or sparsity.
