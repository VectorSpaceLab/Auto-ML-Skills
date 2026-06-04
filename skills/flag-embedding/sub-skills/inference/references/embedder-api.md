# Embedder API Reference

Read this for verified FlagEmbedding embedder signatures, return types, and examples.

## Auto Loader

Verified signature:

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

For mapped model basenames, the loader fills in class, pooling, trust-remote-code, and query-instruction format. For custom local checkpoints, pass `model_class` and usually `pooling_method`.

## `FlagModel`

Use for encoder-only dense embedders.

Verified constructor:

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

Methods:

```python
encode(sentences, batch_size=None, max_length=None, convert_to_numpy=None, **kwargs)
encode_queries(queries, batch_size=None, max_length=None, convert_to_numpy=None, **kwargs)
encode_corpus(corpus, batch_size=None, max_length=None, convert_to_numpy=None, **kwargs)
```

`encode_queries()` applies query instruction handling. `encode_corpus()` is for passages and uses `passage_max_length` by default.

## `BGEM3FlagModel`

Use for `BAAI/bge-m3` dense, lexical sparse, and ColBERT-style representations.

Verified constructor:

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

Encode methods return a dictionary whose keys depend on requested modes:

```text
dense_vecs       numpy array
lexical_weights  list[dict[str, float]]
colbert_vecs     list[numpy array]
```

Score helpers:

```python
compute_score(
    sentence_pairs,
    batch_size=None,
    max_query_length=None,
    max_passage_length=None,
    weights_for_different_modes=None,
    **kwargs,
) -> dict

compute_lexical_matching_score(lexical_weights_1, lexical_weights_2)
```

M3 `compute_score()` can return mode-specific scores such as `dense`, `sparse`, `colbert`, `sparse+dense`, and `colbert+sparse+dense`.

## Decoder-Only Embedders

`FlagLLMModel` verified constructor:

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

Each ICL example should include `instruct`, `query`, and `response` keys.

`FlagPseudoMoEModel` verified constructor defaults include `use_fp16=False`, `use_bf16=True`, `trust_remote_code=True`, and `domain_for_pseudo_moe: str | None = None`.

## Examples

### Custom Encoder Checkpoint

```python
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned(
    "./my-bge-checkpoint",
    model_class="encoder-only-base",
    pooling_method="cls",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ",
    use_fp16=True,
)
```

### M3 Hybrid Representations

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
queries = model.encode_queries(
    ["hybrid retrieval"],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)
corpus = model.encode_corpus(
    ["dense and sparse retrieval can be combined"],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=False,
)
dense_scores = queries["dense_vecs"] @ corpus["dense_vecs"].T
sparse_score = model.compute_lexical_matching_score(
    queries["lexical_weights"][0],
    corpus["lexical_weights"][0],
)
```

### ICL Embedder

```python
from FlagEmbedding import FlagICLModel

examples = [
    {
        "instruct": "Given a web search query, retrieve relevant passages that answer the query.",
        "query": "what is a virtual interface",
        "response": "A virtual interface is a software-defined abstraction of a network interface.",
    }
]
model = FlagICLModel(
    "BAAI/bge-en-icl",
    query_instruction_for_retrieval="Given a question, retrieve passages that answer the question.",
    query_instruction_format="<instruct>{}\n<query>{}",
    examples_for_task=examples,
    examples_instruction_format="<instruct>{}\n<query>{}\n<response>{}",
    use_fp16=True,
)
```

## Gotchas

`normalize_embeddings=True` controls returned vectors, not model training. With normalized vectors, inner product is cosine similarity.

`truncate_dim` is useful for Matryoshka Representation Learning models. Do not truncate arbitrary embeddings unless the model supports meaningful prefix dimensions.

Passing `devices=["cuda:0", "cuda:1"]` can enable multi-device inference for supported classes. If a device error occurs, first retry with one device and smaller batch sizes.
