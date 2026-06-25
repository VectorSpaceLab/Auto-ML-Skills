# Inference Model Selection

This reference helps choose the concrete FlagEmbedding inference class and runtime options. For broader RAG architecture decisions, route to the model-catalog/RAG skill; this page stays focused on API-level inference choices.

## Auto Mapping Versus Explicit Class

`FlagAutoModel.from_finetuned()` and `FlagAutoReranker.from_finetuned()` inspect the basename of `model_name_or_path`. If the basename starts with `checkpoint-`, they inspect the parent directory basename. The basename must appear in the corresponding auto mapping unless `model_class` is provided.

Use auto mapping when:

- The checkpoint is a released model id known to FlagEmbedding, such as `BAAI/bge-m3` or `BAAI/bge-reranker-base`.
- You want FlagEmbedding to choose pooling, trust-remote-code, and instruction format defaults from its mapping.

Use explicit `model_class` when:

- The checkpoint is a local fine-tuned directory with a custom name.
- The checkpoint is a renamed copy of a supported architecture.
- The auto loader raises `Model name ... not found in the model mapping`.
- You need to force a concrete architecture while preserving a local path.

## Embedder Class Choices

| `model_class` | Concrete class | Typical use | Pooling |
| --- | --- | --- | --- |
| `encoder-only-base` | `FlagModel` | BGE/E5/GTE encoder-only dense embeddings | usually `cls` or `mean` |
| `encoder-only-m3` | `BGEM3FlagModel` | BGE-M3 dense+sparse+ColBERT retrieval | `cls` |
| `decoder-only-base` | `FlagLLMModel` | LLM embedding checkpoints | `last_token` |
| `decoder-only-icl` | `FlagICLModel` | In-context-learning embedding checkpoints | `last_token` |
| `decoder-only-pseudo_moe` | `FlagPseudoMoEModel` | Pseudo-MoE compatible embedding checkpoints | `last_token` |

When explicit `model_class` is used, also pass `pooling_method` and `query_instruction_format` if you know the original architecture. The auto loader otherwise falls back to class defaults such as default pooling and `"{}{}"` instruction format.

## Reranker Class Choices

| `model_class` | Concrete class | Typical use |
| --- | --- | --- |
| `encoder-only-base` | `FlagReranker` | BGE reranker base/large/v2-m3 style sequence classification |
| `decoder-only-base` | `FlagLLMReranker` | Decoder-only LLM reranking |
| `decoder-only-layerwise` | `LayerWiseFlagLLMReranker` | Layer-selective reranking with `cutoff_layers` |
| `decoder-only-lightweight` | `LightWeightFlagLLMReranker` | Compressed/lightweight reranking with `compress_ratio` and `compress_layers` |

For local reranker checkpoints, the safest first attempt is to match the class used by the base model that was fine-tuned.

## Known Auto-Mapped Families

The installed mapping includes these embedder families: BGE, Qwen3-Embedding, E5, GTE, SFR, Linq, and BCE. It includes BGE rerankers plus selected third-party reranker ids such as Jina, GTE multilingual reranker, and BCE reranker names. The mapping is version-specific, so use `scripts/check_inference_env.py --show-mappings` to inspect what the current installation exposes without downloading models.

## Instruction Selection

Instruction settings affect only text formatting before tokenization.

- `query_instruction_for_retrieval` applies through `encode_queries()`.
- `passage_instruction_for_retrieval` can be passed as a construction kwarg and applies through `encode_corpus()`.
- `query_instruction_for_rerank` and `passage_instruction_for_rerank` format the two sides before reranker scoring.
- `query_instruction_format` and `passage_instruction_format` need two replacement slots: one for the instruction and one for the original text.
- Formats containing literal `"\\n"` are converted to newline characters by the base classes.

Common patterns:

```python
query_instruction_format="{}{}"
query_instruction_format="Instruct: {}\nQuery: {}"
query_instruction_format="<instruct>{}\n<query>{}"
```

## Similarity And Normalization Choices

For dense embedders:

- `normalize_embeddings=True` is the common retrieval default.
- Dot product on normalized vectors is equivalent to cosine similarity ranking.
- `normalize_embeddings=False` preserves raw vector magnitudes; use only when downstream scoring expects them.

For rerankers:

- `compute_score(..., normalize=False)` returns raw model scores/logits.
- `compute_score(..., normalize=True)` applies sigmoid normalization to produce `[0, 1]`-like scores.
- Use raw scores for relative ranking if the downstream system was calibrated on logits.
- Use normalized scores for display or simple thresholding, but do not assume they are globally calibrated probabilities.

## Pooling And Truncation

- `pooling_method="cls"`: common for many BGE encoder-only models.
- `pooling_method="mean"`: common for E5-style encoder-only models.
- `pooling_method="last_token"`: common for decoder-only LLM embedders.
- `truncate_dim=N`: truncates compatible embedding outputs to dimension `N`, useful for Matryoshka-style embeddings or smaller vector indexes.

If a local checkpoint was fine-tuned from a known base, copy the base model's pooling and instruction format. If unknown, inspect the training config or test retrieval quality before committing to a pooling method.

## Device Resolution

If `devices` is `None`, FlagEmbedding checks hardware in this order:

1. CUDA GPUs, returning all CUDA devices.
2. Torch NPU devices.
3. MUSA devices.
4. MPS devices.
5. CPU.

Explicit device forms:

- `devices="cpu"`: force CPU.
- `devices="cuda:0"`: force one CUDA GPU.
- `devices=["cuda:0", "cuda:1"]`: use multiple devices with multi-process encoding/scoring for list inputs.
- `devices=0` or `devices=[0, 1]`: converted to `cuda:0`/`cuda:1` unless MUSA is available.

Use explicit strings in generated examples to avoid surprises. Integer devices are concise but can unintentionally select CUDA when the user meant CPU.

## Precision Selection

- CPU: use `use_fp16=False`, `use_bf16=False`.
- CUDA: `use_fp16=True` can speed up inference with slight quality differences; verify hardware and model compatibility.
- BF16: use `use_bf16=True` only when the target accelerator supports bfloat16 well.
- Layerwise and lightweight decoder rerankers may warn and force a half precision mode because of model constraints; record that behavior when debugging.

## Batch And Length Selection

Embedders:

- Constructor defaults are `batch_size=256`, `query_max_length=512`, `passage_max_length=512`.
- For short search queries, per-call `max_length=128` or `256` is often enough.
- For long passages, keep `passage_max_length` high enough to preserve relevant context.

Rerankers:

- Constructor default is `batch_size=128`, `query_max_length=None`, and `max_length=512`.
- Many reranker examples use `query_max_length=256` and `max_length=512`.
- Lower `batch_size` first when memory errors occur.

## Trust Remote Code

Auto mappings may set `trust_remote_code=True` for model families that require custom Hugging Face code. Explicit `model_class` defaults `trust_remote_code` to false if not provided. Only enable `trust_remote_code=True` for trusted model sources and after considering the execution risk of remote model code.
