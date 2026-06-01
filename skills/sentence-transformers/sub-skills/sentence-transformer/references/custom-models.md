# Custom SentenceTransformer Models

Read this when a task asks for custom embedding architectures, custom modules, multimodal routing, saving/loading model directories, or converting a plain Transformers checkpoint into a Sentence Transformer.

## Standard Module Chain

Most dense embedding models are sequential module chains:

1. `Transformer`: tokenizes/processes inputs and produces contextual token embeddings.
2. `Pooling`: turns token embeddings into one sentence/document embedding.
3. Optional `Dense`: projects embeddings.
4. Optional `Normalize`: normalizes embeddings for cosine/dot retrieval.

Example:

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import Normalize, Pooling, Transformer

transformer = Transformer("sentence-transformers/all-MiniLM-L6-v2", max_seq_length=256)
pooling = Pooling(transformer.get_embedding_dimension(), pooling_mode="mean")
normalize = Normalize()
model = SentenceTransformer(modules=[transformer, pooling, normalize])
```

When initializing `SentenceTransformer("google-bert/bert-base-uncased")`, the library creates a `Transformer` plus mean `Pooling` by default. Causal language models use last-token pooling by default.

## Static Embeddings

`StaticEmbedding` models skip attention and are CPU-friendly. They are useful when throughput matters more than contextual nuance.

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import StaticEmbedding
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("google-bert/bert-base-uncased")
static_embedding = StaticEmbedding(tokenizer, embedding_dim=512)
model = SentenceTransformer(modules=[static_embedding])
```

## Multimodal Models

The built-in `Transformer` module can detect modalities from a compatible processor. A multimodal model may support `text`, `image`, `audio`, `video`, and `message`.

```python
model = SentenceTransformer(
    "Qwen/Qwen3-VL-Embedding-2B",
    model_kwargs={"torch_dtype": "bfloat16"},
    processor_kwargs={"min_pixels": 28 * 28, "max_pixels": 600 * 600},
)
print(model.modalities)
```

For a composed multimodal model, use `Router` to route different modalities or query/document paths through different modules.

## Custom Module Requirements

A non-input module must implement:

- `forward(features: dict) -> dict`
- `save(output_path: str) -> None`

An input module should implement:

- `preprocess(inputs, prompt=None, **kwargs) -> dict`
- `forward(features: dict) -> dict`
- `save(output_path: str) -> None`

Useful optional methods/properties:

- `load(...)`
- `get_embedding_dimension()`
- `max_seq_length`
- `modalities`

For new code, implement `preprocess`; older `tokenize`-style APIs are backward compatibility.

## Saved Model Layout

`save_pretrained` writes a self-contained model directory with:

- `modules.json`: module order, paths, and class types.
- `config_sentence_transformers.json`: model type, prompts, default prompt, similarity function, and package versions.
- module-specific folders such as `1_Pooling/`.
- tokenizer/config/model weight files, often in the root for the first transformer module.
- `README.md` model card when `create_model_card=True`.

When debugging a saved model, inspect `modules.json` first. If a custom module cannot load, the import path in `modules.json` must be importable in the target environment.

## Prompt And Router Pitfalls

Prompt-aware models may store `prompts` and `default_prompt_name` in `config_sentence_transformers.json`. Query/document prompts matter for retrieval.

Router-based models can route by task or modality. If retrieval quality drops after custom composition, verify that `encode_query` and `encode_document` hit the intended routes.

## When To Avoid Custom Modules

Do not create a custom module when a standard `Transformer`, `Pooling`, `Dense`, `Normalize`, `StaticEmbedding`, or `Router` composition covers the task. Custom modules make Hub reuse and downstream loading more fragile unless the code is packaged and importable.
