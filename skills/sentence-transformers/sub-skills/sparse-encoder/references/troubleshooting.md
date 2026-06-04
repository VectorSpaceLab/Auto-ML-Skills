# SparseEncoder Troubleshooting

## Sparse Tensors Become Huge

Avoid dense conversion for large corpora. Keep `convert_to_sparse_tensor=True` and use search engines or sparse-aware storage.

For quick experiments, small dense conversion can be acceptable, but it does not scale to vocabulary-sized vectors over many documents.

## Scores Are Not Between 0 And 1

Sparse dot-product scores are not probabilities. Large positive scores can be normal. Compare scores within the same query/model/index setup, not across unrelated models.

## Retrieval Misses Obvious Keyword Matches

Check that query and document encoding use the correct methods:

```python
query_embeddings = model.encode_query(queries)
doc_embeddings = model.encode_document(documents)
```

Inspect decoded query/document terms:

```python
print(model.decode(query_embeddings[0], top_k=20))
print(model.decode(doc_embeddings[0], top_k=20))
```

If exact keyword matching is critical, consider hybrid retrieval with BM25 or a lexical search engine.

## Search Engine Integration Fails

Confirm:

- the external Python client is installed;
- the service is reachable;
- the index/collection supports sparse vectors;
- sparse vector indices and values are serialized in the format expected by the engine;
- document ids in search results map back to your corpus.

## `decode` Shows Subword Tokens

Sparse dimensions are tokenizer vocabulary entries. Subword tokens are expected for WordPiece/BPE tokenizers.

## Sparse Training Produces Dense-Looking Vectors

For SPLADE, ensure the training loss is wrapped in `SpladeLoss` or `CachedSpladeLoss` with regularization. Inspect `SparseEncoder.sparsity(...)` during evaluation.

## `max_active_dims` Hurts Recall

Reducing active dimensions lowers index size and latency but can remove useful expansion terms. Evaluate retrieval metrics at several values rather than choosing blindly.
