# RAG Recipes

Use these recipes to plan retrieval-augmented generation with FlagEmbedding model choices. Keep framework-specific application code outside this sub-skill; after planning, route concrete FlagEmbedding calls to `../inference/`.

## Baseline Dense RAG

1. Select an embedder from `model-catalog.md` based on language, latency, and context length.
2. Encode corpus passages with corpus encoding, usually without query instructions.
3. Encode user queries with query encoding and the selected query instruction.
4. Retrieve a candidate set by vector similarity from the target index or vector database.
5. Send the top candidates to the generation layer as grounded context, with citations or source ids preserved by the application.

Good defaults:

- English: `BAAI/bge-base-en-v1.5` for balance; `small` for low cost; `large` for quality.
- Chinese: `BAAI/bge-base-zh-v1.5` for balance.
- Multilingual or long-document retrieval: `BAAI/bge-m3`.

## Retrieve Then Rerank

Use reranking when first-stage retrieval returns plausible but noisy candidates or the final answer quality depends on precise top ordering.

1. Retrieve top 50-200 candidates with an embedder or hybrid retriever.
2. Build `(query, passage)` pairs for the candidate passages.
3. Score pairs with a reranker family from `model-catalog.md`.
4. Sort by reranker score and keep the final top 3-20 for the answer context.
5. Route the concrete `compute_score` implementation to `../inference/`.

Model choice:

- Use `BAAI/bge-reranker-v2-m3` as a practical multilingual reranker default.
- Use `BAAI/bge-reranker-base` or `BAAI/bge-reranker-large` for Chinese/English cross-encoder reranking.
- Use Gemma, layerwise, or lightweight LLM rerankers when quality or multilingual breadth matters enough to justify heavier serving controls.

## BGE-M3 Hybrid Retrieval

BGE-M3 can provide three retrieval signals:

- **Dense vectors**: compact semantic retrieval; easiest to plug into standard vector search.
- **Sparse lexical weights**: token-weighted lexical matching; useful when exact terms, identifiers, or rare words matter.
- **ColBERT-style multi-vectors**: late-interaction fine-grained matching; stronger but heavier to store and score.

Planning pattern:

1. Use dense retrieval as the simplest first-stage path.
2. Add sparse lexical scoring when exact names, product codes, biomedical terms, legal citations, or multilingual term matching are important.
3. Add multi-vector scoring when fine-grained passage matching justifies additional storage and compute.
4. Combine scores only after normalizing and validating scale on a representative query set; weights are task-specific.
5. Optionally apply a reranker after hybrid retrieval for final top-k ordering.

## Multilingual RAG

1. Prefer `BAAI/bge-m3` when one model must handle many languages, long inputs, and hybrid retrieval.
2. Prefer `BAAI/bge-multilingual-gemma2` when an LLM-style multilingual embedder and task instructions are desired.
3. Use a multilingual reranker such as `BAAI/bge-reranker-v2-m3` for final ranking.
4. Keep query instructions in the user's task language when possible, or use a clear English task instruction if the family examples recommend it.
5. Evaluate retrieval quality per language; multilingual training coverage can be uneven.

## LangChain And LlamaIndex Boundaries

FlagEmbedding supplies embedding and reranking models; LangChain, LlamaIndex, vector databases, and application frameworks supply orchestration, storage, prompt construction, and agent loops.

When integrating with a framework:

- Keep the FlagEmbedding model id, query instruction, `model_class`, `trust_remote_code`, and reranker choice explicit.
- Confirm extra framework packages are installed separately; they are not implied by the base FlagEmbedding package.
- Avoid copying notebook-only setup into production code without replacing paths, secrets, vector store configuration, and dependency installation.
- Treat framework callbacks and schema objects as application concerns, not FlagEmbedding model-selection concerns.
