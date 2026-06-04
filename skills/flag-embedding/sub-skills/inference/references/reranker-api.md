# Reranker API Reference

Read this for verified FlagEmbedding reranker signatures, score behavior, and examples.

## Auto Loader

Verified signature:

```python
FlagAutoReranker.from_finetuned(
    model_name_or_path: str,
    model_class: str | RerankerModelClass | None = None,
    use_fp16: bool = False,
    trust_remote_code: bool | None = None,
    **kwargs,
)
```

Auto mapping is based on the basename of `model_name_or_path`. For local checkpoints or unsupported names, pass `model_class`.

## Encoder-Only Reranker

Use `FlagReranker` for `BAAI/bge-reranker-base`, `BAAI/bge-reranker-large`, `BAAI/bge-reranker-v2-m3`, and mapped sequence-classification rerankers.

Verified constructor:

```python
FlagReranker(
    model_name_or_path: str,
    use_fp16: bool = False,
    query_instruction_for_rerank: str | None = None,
    query_instruction_format: str = "{}{}",
    passage_instruction_for_rerank: str | None = None,
    passage_instruction_format: str = "{}{}",
    trust_remote_code: bool = False,
    cache_dir: str | None = None,
    devices: str | list[str] | list[int] | None = None,
    batch_size: int = 128,
    query_max_length: int | None = None,
    max_length: int = 512,
    normalize: bool = False,
    **kwargs,
)
```

Methods:

```python
compute_score(sentence_pairs, **kwargs)
compute_score_single_gpu(
    sentence_pairs,
    batch_size=None,
    query_max_length=None,
    max_length=None,
    normalize=None,
    device=None,
    **kwargs,
) -> list[float]
```

`sentence_pairs` can be one pair like `["query", "passage"]` or a list of pairs.

## LLM Rerankers

`FlagLLMReranker` verified constructor:

```python
FlagLLMReranker(
    model_name_or_path: str,
    peft_path: str | None = None,
    use_fp16: bool = False,
    use_bf16: bool = False,
    query_instruction_for_rerank: str = "A: ",
    query_instruction_format: str = "{}{}",
    passage_instruction_for_rerank: str = "B: ",
    passage_instruction_format: str = "{}{}",
    cache_dir: str | None = None,
    trust_remote_code: bool = False,
    devices=None,
    prompt: str | None = None,
    batch_size: int = 128,
    query_max_length: int | None = None,
    max_length: int = 512,
    normalize: bool = False,
    **kwargs,
)
```

`LayerWiseFlagLLMReranker` adds:

```python
cutoff_layers: list[int] | None = None
```

Score-time calls can also pass `cutoff_layers=[28]` or another chosen layer list.

`LightWeightFlagLLMReranker` adds:

```python
cutoff_layers: list[int] | None = None
compress_layers: list[int] = [8]
compress_ratio: int = 1
```

Score-time calls can pass `cutoff_layers`, `compress_ratio`, and `compress_layers`.

## Examples

### Auto Reranker

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=True,
)
pairs = [
    ["what is panda?", "hi"],
    ["what is panda?", "The giant panda is a bear species endemic to China."],
]
scores = reranker.compute_score(pairs)
prob_like = reranker.compute_score(pairs, normalize=True)
```

`normalize=True` applies a sigmoid transform to map scores into `[0, 1]`. The normalized value is useful for ranking display, but it is not a calibrated probability unless separately calibrated.

### Custom Encoder Reranker Checkpoint

```python
from FlagEmbedding import FlagAutoReranker

reranker = FlagAutoReranker.from_finetuned(
    "./my-reranker-checkpoint",
    model_class="encoder-only-base",
    query_max_length=256,
    max_length=512,
)
```

### Layerwise Reranker

```python
from FlagEmbedding import LayerWiseFlagLLMReranker

reranker = LayerWiseFlagLLMReranker(
    "BAAI/bge-reranker-v2-minicpm-layerwise",
    use_fp16=True,
)
scores = reranker.compute_score(
    [["query", "passage"]],
    cutoff_layers=[28],
)
```

### Lightweight Reranker

```python
from FlagEmbedding import LightWeightFlagLLMReranker

reranker = LightWeightFlagLLMReranker(
    "BAAI/bge-reranker-v2.5-gemma2-lightweight",
    use_fp16=True,
)
scores = reranker.compute_score(
    [["query", "passage"]],
    cutoff_layers=[28],
    compress_ratio=2,
    compress_layers=[24, 40],
)
```

## Gotchas

Rerankers should usually process top-k results from a retriever, not an entire corpus.

The constructor argument for maximum sequence length is `max_length` in the Python API. Some evaluation and helper scripts expose it as `reranker_max_length`.

`query_max_length` can be `None`, letting the model/truncation logic use the combined `max_length`. Set it explicitly for long passages when query truncation must be controlled.

LLM rerankers can be slow and memory-heavy. Use small `batch_size`, `max_length`, and explicit devices for first runs.
