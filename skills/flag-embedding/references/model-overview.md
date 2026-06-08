# Model Overview

Read this when choosing a FlagEmbedding model family, explicit `model_class`, pooling method, or reranker class. The facts here were distilled from package metadata, public README/examples, source mappings, tests, and live installed-package inspection.

## Install Variants

- `pip install -U FlagEmbedding`: inference, reranking, and evaluation imports.
- `pip install -U "FlagEmbedding[finetune]"`: training workflows that need optional `deepspeed` and `flash-attn`.
- Evaluation examples often require extra packages such as `mteb`, `beir`, `pytrec_eval` or `pytrec-eval-terrier`, `faiss`, and `air-benchmark` depending on the benchmark.

## Embedder Families

Use `FlagAutoModel.from_finetuned(model_name_or_path, ...)` when the model id basename is known by the package. If the model name is unknown, specify `model_class`.

Verified embedder `model_class` values:

| Value | Class family | Typical use |
| --- | --- | --- |
| `encoder-only-base` | `FlagModel` | BGE v1/v1.5 encoder embedders and similar encoder-only checkpoints. |
| `encoder-only-m3` | `BGEM3FlagModel` | `BAAI/bge-m3`; dense, sparse lexical, and ColBERT-style multi-vector outputs. |
| `decoder-only-base` | `FlagLLMModel` | LLM-based embedding models such as multilingual Gemma2 or Qwen/GTE/SFR style instruct embeddings. |
| `decoder-only-icl` | `FlagICLModel` | `BAAI/bge-en-icl` style in-context-learning embedding. |
| `decoder-only-pseudo_moe` | `FlagPseudoMoEModel` | Pseudo-MoE decoder-only embedding variants. |

Known auto embedder model ids include BGE models such as `bge-m3`, `bge-base-en-v1.5`, `bge-large-en-v1.5`, `bge-small-zh-v1.5`, `bge-en-icl`, `bge-multilingual-gemma2`, `bge-code-v1`, and `bge-reasoner-embed-qwen3-8b-0923`, plus Qwen3, E5, GTE, SFR, Linq, and BCE mappings.

## Reranker Families

Use `FlagAutoReranker.from_finetuned(model_name_or_path, ...)` for known reranker ids. Use explicit `model_class` for local checkpoints, renamed checkpoints, or custom models.

Verified reranker `model_class` values:

| Value | Class family | Typical use |
| --- | --- | --- |
| `encoder-only-base` | `FlagReranker` | Cross-encoder rerankers such as `bge-reranker-base`, `bge-reranker-large`, `bge-reranker-v2-m3`. |
| `decoder-only-base` | `FlagLLMReranker` | LLM rerankers such as `bge-reranker-v2-gemma`. |
| `decoder-only-layerwise` | `LayerWiseFlagLLMReranker` | Layer-selectable rerankers such as `bge-reranker-v2-minicpm-layerwise`. |
| `decoder-only-lightweight` | `LightWeightFlagLLMReranker` | Lightweight compression rerankers such as `bge-reranker-v2.5-gemma2-lightweight`. |

Known auto reranker ids include `bge-reranker-base`, `bge-reranker-large`, `bge-reranker-v2-m3`, `bge-reranker-v2-gemma`, `bge-reranker-v2-minicpm-layerwise`, `bge-reranker-v2.5-gemma2-lightweight`, `jinaai/jina-reranker-v2-base-multilingual`, `Alibaba-NLP/gte-multilingual-reranker-base`, `maidalun1020/bce-reranker-base_v1`, and `jinaai/jina-reranker-v1-turbo-en`.

## Instructions And Pooling

For short-query to long-passage retrieval, use `encode_queries()` for queries and `encode_corpus()` for passages. `encode_queries()` applies `query_instruction_for_retrieval` when configured; passages normally need no query instruction.

Common BGE English v1.5 query instruction:

```text
Represent this sentence for searching relevant passages:
```

Common BGE Chinese v1.5 query instruction:

```text
为这个句子生成表示以用于检索相关文章：
```

Common pooling values are `cls`, `mean`, and `last_token`. Auto mappings choose defaults for known models; for custom checkpoints pass `pooling_method` explicitly.

## Device Selection

If `devices` is omitted, FlagEmbedding chooses all visible CUDA devices, then NPU, MUSA, MPS, and finally CPU. Pass `devices="cpu"` for a deterministic CPU-only path, `devices="cuda:0"` for one GPU, or `devices=["cuda:0", "cuda:1"]` for multi-process inference.

Use `use_fp16=True` primarily on GPU. On CPU, set `use_fp16=False` if the model or torch operation does not support half precision.

## Choosing A Workflow

- Embed and compare text vectors: inference sub-skill, `FlagAutoModel` or `FlagModel`.
- Need dense+sparse+multi-vector retrieval: inference sub-skill, `BGEM3FlagModel`.
- Need direct query-passage relevance scores: inference sub-skill, `FlagAutoReranker` or reranker class.
- Need to adapt a model on retrieval data: finetuning sub-skill.
- Need benchmark or custom dataset metrics: evaluation sub-skill.
