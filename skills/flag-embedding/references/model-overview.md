# Model Overview

Read this when selecting a model, deciding whether `model_class` is required, or explaining auto-mapping behavior.

## Embedder Model Classes

`FlagAutoModel.from_finetuned(..., model_class=...)` accepts these verified class identifiers:

| `model_class` | Concrete class | Use for |
| --- | --- | --- |
| `encoder-only-base` | `FlagModel` | BGE v1/v1.5, E5, GTE, BCE style encoder embedders |
| `encoder-only-m3` | `BGEM3FlagModel` | `BAAI/bge-m3` dense, sparse, and ColBERT-style outputs |
| `decoder-only-base` | `FlagLLMModel` | LLM-based embedding models such as Gemma/Qwen/Mistral families |
| `decoder-only-icl` | `FlagICLModel` | In-context-learning embedding models such as `BAAI/bge-en-icl` |
| `decoder-only-pseudo_moe` | `FlagPseudoMoEModel` | Pseudo-MoE decoder-only embeddings; pass `domain_for_pseudo_moe` when needed |

If the model is in the auto mapping, `model_class`, pooling method, trust-remote-code, and query-instruction format are inferred. If a local checkpoint or new Hugging Face model name is not mapped, pass `model_class` and often `pooling_method` explicitly.

## Common Embedder Auto Mappings

Selected verified mappings:

| Model basename | Class | Pooling | `trust_remote_code` | Query format |
| --- | --- | --- | --- | --- |
| `bge-m3` | `BGEM3FlagModel` | `cls` | `False` | `{}` + `{}` |
| `bge-large-en-v1.5`, `bge-base-en-v1.5`, `bge-small-en-v1.5` | `FlagModel` | `cls` | `False` | `{}` + `{}` |
| `bge-large-zh-v1.5`, `bge-base-zh-v1.5`, `bge-small-zh-v1.5` | `FlagModel` | `cls` | `False` | `{}` + `{}` |
| `bge-en-icl` | `FlagICLModel` | `last_token` | `False` | `<instruct>{}\n<query>{}` |
| `bge-multilingual-gemma2` | `FlagLLMModel` | `last_token` | `False` | `<instruct>{}\n<query>{}` |
| `bge-code-v1` | `FlagLLMModel` | `last_token` | `True` | `<instruct>{}\n<query>{}` |
| `bge-reasoner-embed-qwen3-8b-0923` | `FlagLLMModel` | `last_token` | `False` | `Instruct: {}\nQuery: {}` |
| `Qwen3-Embedding-0.6B`, `Qwen3-Embedding-4B`, `Qwen3-Embedding-8B` | `FlagLLMModel` | `last_token` | `False` | `Instruct: {}\nQuery:{}` |
| `e5-large-v2`, `e5-base-v2`, `e5-small-v2` | `FlagModel` | `mean` | `False` | `{}` + `{}` |
| `multilingual-e5-large-instruct` | `FlagModel` | `mean` | `False` | `Instruct: {}\nQuery: {}` |
| `gte-Qwen2-7B-instruct`, `gte-Qwen2-1.5B-instruct`, `gte-Qwen1.5-7B-instruct` | `FlagLLMModel` | `last_token` | `True` | `Instruct: {}\nQuery: {}` |
| `gte-multilingual-base`, `gte-large-en-v1.5`, `gte-base-en-v1.5` | `FlagModel` | `cls` | `True` | `{}` + `{}` |
| `SFR-Embedding-2_R`, `SFR-Embedding-Mistral`, `Linq-Embed-Mistral` | `FlagLLMModel` | `last_token` | `False` | `Instruct: {}\nQuery: {}` |
| `bce-embedding-base_v1` | `FlagModel` | `cls` | `False` | `{}` + `{}` |

Run `scripts/print_model_mappings.py` from the root skill to inspect the installed package's full current mapping.

## Reranker Model Classes

`FlagAutoReranker.from_finetuned(..., model_class=...)` accepts these verified class identifiers:

| `model_class` | Concrete class | Use for |
| --- | --- | --- |
| `encoder-only-base` | `FlagReranker` | XLM-R/BGE-M3 sequence-classification rerankers |
| `decoder-only-base` | `FlagLLMReranker` | LLM-based yes/no rerankers |
| `decoder-only-layerwise` | `LayerWiseFlagLLMReranker` | Layerwise LLM rerankers with `cutoff_layers` |
| `decoder-only-lightweight` | `LightWeightFlagLLMReranker` | Lightweight LLM rerankers with `cutoff_layers`, `compress_ratio`, and `compress_layers` |

## Common Reranker Auto Mappings

| Model | Class | Notes |
| --- | --- | --- |
| `bge-reranker-base` | `FlagReranker` | Chinese and English encoder reranker |
| `bge-reranker-large` | `FlagReranker` | Larger encoder reranker |
| `bge-reranker-v2-m3` | `FlagReranker` | Multilingual BGE-M3 based reranker |
| `bge-reranker-v2-gemma` | `FlagLLMReranker` | LLM reranker |
| `bge-reranker-v2-minicpm-layerwise` | `LayerWiseFlagLLMReranker` | Use `cutoff_layers` for scoring layers |
| `bge-reranker-v2.5-gemma2-lightweight` | `LightWeightFlagLLMReranker` | Use `cutoff_layers`, `compress_ratio`, `compress_layers` |
| `jinaai/jina-reranker-v2-base-multilingual` | `FlagReranker` | Non-BGE supported reranker |
| `Alibaba-NLP/gte-multilingual-reranker-base` | `FlagReranker` | Non-BGE supported reranker |
| `maidalun1020/bce-reranker-base_v1` | `FlagReranker` | Non-BGE supported reranker |

## Selection Heuristics

For general dense retrieval with small or medium encoder models, start with `BAAI/bge-base-en-v1.5`, `BAAI/bge-base-zh-v1.5`, or the appropriate large/small sibling.

For multilingual and multi-function retrieval, use `BAAI/bge-m3` with `BGEM3FlagModel` or `FlagAutoModel`. It can return dense vectors, lexical weights, and ColBERT vectors.

For query tasks needing prompts or in-context examples, use LLM-based embedders such as `BAAI/bge-multilingual-gemma2` or `BAAI/bge-en-icl`.

For reranking top-k retrieved documents, start with `BAAI/bge-reranker-v2-m3`. Use LLM rerankers when accuracy is more important than latency and GPU memory allows it.

For local fine-tuned checkpoints, infer the class from the base model architecture and pass `model_class`. Auto mapping uses the basename of `model_name_or_path`; checkpoint directories named `checkpoint-*` are resolved to the parent basename.
