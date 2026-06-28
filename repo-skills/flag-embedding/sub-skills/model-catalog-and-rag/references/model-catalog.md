# Model Catalog

This catalog distills common FlagEmbedding auto-mapping and README guidance into model-selection rules. Use it to choose model families and `model_class`; route concrete loading and scoring code to `../inference/`.

## Embedder Families

| Need | Recommended family | Typical model ids | Auto class | `model_class` for custom checkpoints | Notes |
| --- | --- | --- | --- | --- | --- |
| English dense retrieval, practical default | BGE v1.5 English | `BAAI/bge-small-en-v1.5`, `BAAI/bge-base-en-v1.5`, `BAAI/bge-large-en-v1.5` | `FlagModel` | `encoder-only-base` | CLS pooling; use English retrieval instruction for query-side short-to-passage retrieval. |
| Chinese dense retrieval | BGE v1.5 Chinese | `BAAI/bge-small-zh-v1.5`, `BAAI/bge-base-zh-v1.5`, `BAAI/bge-large-zh-v1.5` | `FlagModel` | `encoder-only-base` | CLS pooling; use the Chinese retrieval instruction for queries. |
| Multilingual, long context, hybrid retrieval | BGE-M3 | `BAAI/bge-m3` | `BGEM3FlagModel` | `encoder-only-m3` | Supports dense, sparse lexical, and ColBERT-style multi-vector outputs; up to long-document retrieval scenarios. |
| Multilingual LLM embedder | BGE Gemma2 | `BAAI/bge-multilingual-gemma2` | `FlagLLMModel` | `decoder-only-base` | Last-token pooling; use instruction format `<instruct>{}\n<query>{}`. |
| English ICL embedder | BGE ICL | `BAAI/bge-en-icl` | `FlagICLModel` | `decoder-only-icl` | Supports task instructions and few-shot examples; use for richer query representation when examples are useful. |
| Qwen3 embedding | Qwen3 | `Qwen3-Embedding-0.6B`, `Qwen3-Embedding-4B`, `Qwen3-Embedding-8B` | `FlagLLMModel` | `decoder-only-base` | Last-token pooling; mapped instruction format is `Instruct: {}\nQuery:{}`. |
| E5 encoder models | E5 | `e5-small-v2`, `e5-base-v2`, `e5-large-v2`, multilingual E5 variants | `FlagModel` | `encoder-only-base` | Mean pooling for most E5 mappings; multilingual instruct variants use `Instruct: {}\nQuery: {}`. |
| GTE encoder or LLM models | GTE | `gte-small`, `gte-base`, `gte-large`, `gte-Qwen2-7B-instruct`, `gte-multilingual-base` | `FlagModel` or `FlagLLMModel` | `encoder-only-base` or `decoder-only-base` | Several GTE mappings require `trust_remote_code=True`; verify this decision before use. |
| Code retrieval | BGE code | `bge-code-v1` | `FlagLLMModel` | `decoder-only-base` | Requires `trust_remote_code=True`; use instruction format `<instruct>{}\n<query>{}`. |

## BGE Dense Model Scale

| Scale | Use when | Tradeoff |
| --- | --- | --- |
| `small` | Low latency, CPU experiments, constrained memory | Fastest and smallest, lower ceiling. |
| `base` | Balanced default for many applications | Good first choice when latency and quality both matter. |
| `large` | Quality is more important than serving cost | Stronger retrieval but higher memory and latency. |

## Reranker Families

| Need | Typical model ids | Auto class | `model_class` for custom checkpoints | Notes |
| --- | --- | --- | --- | --- |
| Chinese/English cross-encoder reranking | `BAAI/bge-reranker-base`, `BAAI/bge-reranker-large` | `FlagReranker` | `encoder-only-base` | Use after initial retrieval; base is lighter, large is stronger. |
| Lightweight multilingual reranking | `BAAI/bge-reranker-v2-m3` | `FlagReranker` | `encoder-only-base` | Practical multilingual default with fast inference. |
| Multilingual LLM reranking | `BAAI/bge-reranker-v2-gemma` | `FlagLLMReranker` | `decoder-only-base` | Higher-capacity reranker; heavier serving profile. |
| Layerwise LLM reranking | `BAAI/bge-reranker-v2-minicpm-layerwise` | `LayerWiseFlagLLMReranker` | `decoder-only-layerwise` | Supports selecting cutoff layers to trade quality and speed. |
| Lightweight/compressed LLM reranking | `BAAI/bge-reranker-v2.5-gemma2-lightweight` | `LightWeightFlagLLMReranker` | `decoder-only-lightweight` | Supports layer and compression controls. |

## Query Instructions

| Family | Query instruction guidance | Format guidance |
| --- | --- | --- |
| BGE English v1/v1.5 | `Represent this sentence for searching relevant passages: ` | Default `{}{}` works: instruction concatenated before query. |
| BGE Chinese v1/v1.5 | `为这个句子生成表示以用于检索相关文章：` | Default `{}{}` works. |
| BGE-M3 | Often works without a query instruction in the mapped configuration | Focus on selecting dense/sparse/multi-vector outputs. |
| BGE Gemma2 / BGE ICL | Provide task-specific retrieval instruction | `<instruct>{}\n<query>{}`. |
| Qwen3 embeddings | Provide task-specific retrieval instruction | `Instruct: {}\nQuery:{}`. |
| E5/GTE instruct variants | Provide task-specific retrieval instruction | Usually `Instruct: {}\nQuery: {}`. |

For short-query-to-long-passage retrieval, use the embedder's query path so the query instruction is applied to queries only. Do not prepend the query instruction to corpus passages unless the model documentation for that specific family says to do so.

## Custom Checkpoint Resolution

1. Identify the base family used to produce the checkpoint.
2. If it is a BGE v1/v1.5-style encoder checkpoint, pass `model_class="encoder-only-base"`.
3. If it is a BGE-M3 checkpoint, pass `model_class="encoder-only-m3"`.
4. If it is a decoder-only embedding checkpoint such as BGE Gemma2, E5 Mistral, Qwen3, or GTE Qwen instruct, pass `model_class="decoder-only-base"` unless the family is explicitly ICL or pseudo-MoE.
5. For rerankers, choose `encoder-only-base`, `decoder-only-base`, `decoder-only-layerwise`, or `decoder-only-lightweight` from the reranker table.
6. If the model requires remote custom modeling files, make a deliberate `trust_remote_code=True` decision and document why.
