# Inference API Reference

Read this for verified public signatures, model-class values, return shapes, and common parameter choices. The signatures were checked against an installed FlagEmbedding package.

## Public Exports

From `FlagEmbedding`:

- `FlagAutoModel`
- `FlagModel`
- `BGEM3FlagModel`
- `FlagLLMModel`
- `FlagICLModel`
- `FlagPseudoMoEModel`
- `FlagAutoReranker`
- `FlagReranker`
- `FlagLLMReranker`
- `LayerWiseFlagLLMReranker`
- `LightWeightFlagLLMReranker`
- `EmbedderModelClass`
- `RerankerModelClass`

## Auto Embedder

```python
FlagAutoModel.from_finetuned(
    model_name_or_path: str,
    model_class: str | EmbedderModelClass | None = None,
    normalize_embeddings: bool = True,
    use_fp16: bool = True,
    use_bf16: bool = False,
    query_instruction_for_retrieval: str | None = None,
    devices: str | list[str] | None = None,
    pooling_method: str | None = None,
    trust_remote_code: bool | None = None,
    query_instruction_format: str | None = None,
    truncate_dim: int | None = None,
    **kwargs,
)
```

`model_name_or_path` can be a local path or Hugging Face model id. Auto mapping uses the basename; for `checkpoint-*` paths it uses the parent basename.

Embedder `model_class` values:

- `encoder-only-base`
- `encoder-only-m3`
- `decoder-only-base`
- `decoder-only-icl`
- `decoder-only-pseudo_moe`

When `model_class` is specified and a default is missing, the loader uses class defaults such as pooling method, `trust_remote_code=False`, and query instruction format `"{}{}"`.

## Embedder Classes

`FlagModel` constructor:

```python
FlagModel(
    model_name_or_path: str,
    normalize_embeddings: bool = True,
    use_fp16: bool = True,
    use_bf16: bool = False,
    query_instruction_for_retrieval: str | None = None,
    query_instruction_format: str = "{}{}",
    devices: str | list[str] | None = None,
    pooling_method: str = "cls",
    trust_remote_code: bool = False,
    cache_dir: str | None = None,
    batch_size: int = 256,
    query_max_length: int = 512,
    passage_max_length: int = 512,
    convert_to_numpy: bool = True,
    truncate_dim: int | None = None,
    **kwargs,
)
```

Core methods inherited from `AbsEmbedder`:

```python
model.encode(sentences, batch_size=None, max_length=None, convert_to_numpy=None, instruction=None, instruction_format=None, **kwargs)
model.encode_queries(queries, batch_size=None, max_length=None, convert_to_numpy=None, **kwargs)
model.encode_corpus(corpus, batch_size=None, max_length=None, convert_to_numpy=None, **kwargs)
```

Return shape:

- Single string: one vector.
- List of strings: two-dimensional array/tensor with first dimension equal to input length.
- `convert_to_numpy=True`: numpy arrays.
- `convert_to_numpy=False`: torch tensors when supported by the concrete implementation.

## BGE-M3

`BGEM3FlagModel` constructor:

```python
BGEM3FlagModel(
    model_name_or_path: str,
    normalize_embeddings: bool = True,
    use_fp16: bool = True,
    use_bf16: bool = False,
    query_instruction_for_retrieval: str | None = None,
    query_instruction_format: str = "{}{}",
    devices: str | list[str] | None = None,
    pooling_method: str = "cls",
    trust_remote_code: bool = False,
    cache_dir: str | None = None,
    colbert_dim: int = -1,
    batch_size: int = 256,
    query_max_length: int = 512,
    passage_max_length: int = 512,
    return_dense: bool = True,
    return_sparse: bool = False,
    return_colbert_vecs: bool = False,
    truncate_dim: int | None = None,
    **kwargs,
)
```

`BGEM3FlagModel.encode(...)`:

```python
encode(
    sentences,
    batch_size=None,
    max_length=None,
    return_dense=None,
    return_sparse=None,
    return_colbert_vecs=None,
    **kwargs,
) -> dict
```

Possible keys:

- `dense_vecs`: dense vectors.
- `lexical_weights`: sparse lexical weights.
- `colbert_vecs`: multi-vector ColBERT-style vectors.

`BGEM3FlagModel.compute_score(...)`:

```python
compute_score(
    sentence_pairs,
    batch_size=None,
    max_query_length=None,
    max_passage_length=None,
    weights_for_different_modes=None,
    **kwargs,
) -> dict
```

Possible score keys include `dense`, `sparse`, `colbert`, `sparse+dense`, and `colbert+sparse+dense`.

## Decoder-Only Embedders

`FlagLLMModel` constructor:

```python
FlagLLMModel(
    model_name_or_path: str,
    normalize_embeddings: bool = True,
    use_fp16: bool = True,
    use_bf16: bool = False,
    query_instruction_for_retrieval: str | None = None,
    query_instruction_format: str = "Instruct: {}\nQuery: {}",
    devices: str | list[str] | None = None,
    trust_remote_code: bool = False,
    cache_dir: str | None = None,
    batch_size: int = 256,
    query_max_length: int = 512,
    passage_max_length: int = 512,
    convert_to_numpy: bool = True,
    truncate_dim: int | None = None,
    **kwargs,
)
```

`FlagICLModel` adds:

```python
suffix: str = "\n<response>"
examples_for_task: list[dict] | None = None
examples_instruction_format: str = "<instruct>{}\n<query>{}\n<response>{}"
```

Use ICL examples only when the model family expects few-shot examples in the query prompt.

## Auto Reranker

```python
FlagAutoReranker.from_finetuned(
    model_name_or_path: str,
    model_class: str | RerankerModelClass | None = None,
    use_fp16: bool = False,
    trust_remote_code: bool | None = None,
    **kwargs,
)
```

Reranker `model_class` values:

- `encoder-only-base`
- `decoder-only-base`
- `decoder-only-layerwise`
- `decoder-only-lightweight`

## Reranker Classes

`FlagReranker` constructor:

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

`compute_score(sentence_pairs, **kwargs)` accepts a single pair such as `["query", "passage"]` or a list of pairs. It returns raw scores by default and normalized sigmoid scores when `normalize=True`.

`FlagLLMReranker` adds `peft_path`, `use_bf16`, default query/passage instruction prefixes `A: ` and `B: `, and optional `prompt`.

`LayerWiseFlagLLMReranker` adds `cutoff_layers`.

`LightWeightFlagLLMReranker` adds `cutoff_layers`, `compress_layers`, and `compress_ratio`.

## Device Values

Accepted device inputs include:

- `None`: automatically choose all visible CUDA devices, then NPU, MUSA, MPS, or CPU.
- String: `"cpu"`, `"cuda:0"`, `"mps"`, etc.
- Integer: GPU index such as `0`.
- List of strings or integers for multi-device inference.

For predictable examples, pass one explicit device.
