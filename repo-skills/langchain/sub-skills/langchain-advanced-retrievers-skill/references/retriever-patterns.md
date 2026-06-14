# Retriever Patterns

Read this to choose the right advanced retriever.

## Strategy Map

| Symptom | Pattern |
| --- | --- |
| Query wording misses relevant chunks | `MultiQueryRetriever` generates query variants. |
| Vector search and keyword search each miss different cases | `EnsembleRetriever` combines retrievers with weights. |
| Small chunks retrieve well but answers need larger context | `ParentDocumentRetriever`. |
| One logical document has summaries, questions, or multimodal vectors | `MultiVectorRetriever`. |
| User queries include metadata constraints | `SelfQueryRetriever`. |
| Retrieved docs are too long or noisy | `ContextualCompressionRetriever` plus compressor/reranker. |
| Recency matters | `TimeWeightedVectorStoreRetriever`. |

## Build Order

1. Prove loaders/splitters create correct `Document` metadata.
2. Prove vector or lexical base retriever returns expected docs for a few queries.
3. Add one advanced strategy.
4. Add LLM-generated query expansion, metadata filters, or compressors last.
5. Keep a no-key smoke path with in-memory stores for regression checks.

## Parent Document Data Shape

Parent retrieval depends on stable ids:

- child chunks are embedded into the vector store
- child metadata stores a parent id under `id_key`, default `doc_id`
- parent documents are stored in `docstore`
- retrieval finds child chunks, then fetches parents by id

If any of those pieces are missing, retrieval may return children, duplicates, or no parents.

## Hybrid Retrieval Tuning

For `EnsembleRetriever`, tune:

- each child retriever's `k`
- `weights`
- `id_key` for deduplication
- lexical tokenizer/stemming outside LangChain when using BM25-style retrievers
- metadata filters before or after ensemble depending on backend support

## LLM-Backed Query Expansion

For `MultiQueryRetriever`, use a low-temperature model and log generated queries. Keep `include_original=True` when expansion quality is uncertain.

## Reranking And Compression

Use compression after recall is acceptable. A compressor/reranker can reduce noise, but it cannot select documents that the base retriever did not return.
