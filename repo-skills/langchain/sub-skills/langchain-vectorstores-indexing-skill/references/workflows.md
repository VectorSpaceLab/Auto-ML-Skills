# Vectorstore And Indexing Workflows

## No-Key In-Memory Index

1. Create `Document` chunks with source metadata.
2. Instantiate `DeterministicFakeEmbedding(size=...)`.
3. Instantiate `InMemoryVectorStore(embedding=embedding)`.
4. Add documents and run `similarity_search`.
5. Convert to retriever with `as_retriever(search_kwargs={"k": 3})`.

## Production Store Checklist

Record these before indexing:

- embedding provider/model and dimension
- collection/index name
- distance metric
- persistence path or service endpoint
- metadata filter schema
- document id/upsert policy
- deletion/stale-document policy

## Retriever Tuning

Start with `k`, then tune backend-specific search type, score threshold, metadata filters, MMR, or hybrid search if the integration supports them.
