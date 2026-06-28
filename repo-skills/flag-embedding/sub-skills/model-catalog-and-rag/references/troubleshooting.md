# Troubleshooting

## Auto Mapping Does Not Recognize A Model

Symptoms: loading through an auto class reports an unknown model name or cannot infer a model class.

Fix:

1. Check whether the checkpoint basename is in the common mapping with `scripts/recommend_model_class.py`.
2. If the checkpoint is custom or renamed, identify the base family used for finetuning.
3. Pass the explicit `model_class` value from `model-catalog.md`.
4. If the checkpoint is a new architecture, route to `../inference/` for implementation details and avoid guessing unsupported class names.

## `trust_remote_code` Is Unclear

Some mapped families require custom modeling code from the model repository. Use `trust_remote_code=True` only when the model family requires it and the source is trusted for the deployment environment.

Common cases that may require it include BGE code models, GTE Qwen instruct models, GTE multilingual/base v1.5 variants, and some local LLM reranker modeling files. If policy forbids remote code, select a family that works without remote custom code.

## Retrieval Quality Is Poor

Checklist:

- The query instruction is missing or mismatched for an instruction-tuned family.
- The query instruction was accidentally prepended to corpus passages.
- The wrong language family was selected for the corpus and queries.
- A reranker was expected to create embeddings; rerankers only score candidate pairs.
- Embeddings are not normalized consistently with the intended similarity function.
- Candidate depth is too shallow before reranking.
- Chunking loses context, metadata, or source ids needed by the generator.

## Reranker Used In Place Of Embedder

Rerankers are cross-encoders or LLM scorers over `(query, passage)` pairs. They do not build the initial vector index and are usually too expensive to score an entire corpus. First retrieve with an embedder or hybrid retriever, then rerank a bounded candidate set.

## BGE-M3 Outputs Are Misunderstood

BGE-M3 can return dense vectors, sparse lexical weights, and ColBERT-style multi-vector outputs. Dense vectors fit ordinary vector search. Sparse weights need lexical/hybrid scoring support. Multi-vectors need late-interaction storage and scoring. Do not assume all three outputs can be inserted into the same vector index without adapter logic.

## Framework Example Fails With Missing Packages

LangChain, LlamaIndex, vector stores, notebooks, and UI demos often require dependencies outside the base FlagEmbedding install. Separate the model plan from the application stack:

1. Prove the FlagEmbedding model and reranker choices independently.
2. Install or configure the framework packages in the application environment.
3. Adapt framework-specific wrappers to preserve query instructions and reranker candidate ordering.
