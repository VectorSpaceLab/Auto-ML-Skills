# Advanced Retriever Troubleshooting

## Parent Retriever Returns Child Chunks

Check that `docstore` is set, parent ids are written under the same `id_key`, and `add_documents()` was called on the `ParentDocumentRetriever`, not only on the vector store.

## Duplicate Documents

Set stable metadata ids and pass `id_key` to `EnsembleRetriever` when combining retrievers that may return the same source.

## `BM25Retriever` Import Fails

Install `langchain-community` and any backend-specific optional dependency required by that retriever. Use vector-only smoke tests until lexical dependencies are present.

## Self Query Generates Invalid Filters

Confirm the vector store supports metadata filtering, the translator matches that backend, and metadata field descriptions are explicit. Start with simple equality filters.

## Multi Query Hurts Precision

Set `include_original=True`, lower model randomness, inspect generated query variants, and reduce the number of variants.

## Compression Drops Needed Context

Increase base retriever `k`, inspect documents before compression, and validate the compressor or reranker independently.
