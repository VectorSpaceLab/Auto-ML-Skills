# Package Overview

Read this when choosing the right public API, install extra, or import path for `sentence-transformers`.

## Public Package Facts

- Distribution: `sentence-transformers`
- Import root: `sentence_transformers`
- Python: 3.10+
- Runtime dependencies include `transformers>=4.41,<6`, `huggingface-hub>=0.23`, `torch>=1.11`, `numpy`, `scikit-learn`, `scipy`, `typing_extensions`, and `tqdm`.
- Main public classes: `SentenceTransformer`, `CrossEncoder`, `SparseEncoder`.
- Backends: PyTorch by default, plus ONNX and OpenVINO for compatible models when the matching extras are installed.

## Install Extras

| Extra | Use |
| --- | --- |
| none | text model loading, saving, and inference |
| `image` | image and vision-language embedding/reranking models |
| `audio` | audio model inputs |
| `video` | video model inputs |
| `train` | trainer workflows with `datasets` and `accelerate` |
| `onnx` | ONNX Runtime CPU export/inference |
| `onnx-gpu` | ONNX Runtime GPU export/inference |
| `openvino` | OpenVINO export/inference |
| `dev` | repository development, tests, multimodal extras |

The extras can be combined, for example:

```bash
pip install -U "sentence-transformers[train,image,onnx-gpu]"
```

For audio/video decoders, some inputs require `torchcodec` separately.

## Model Classes

`SentenceTransformer` is the bi-encoder/dense embedding class. It independently maps each input into a vector and is used for semantic similarity, semantic search, clustering, classification features, paraphrase mining, duplicate detection, and first-stage retrieval.

`CrossEncoder` scores input pairs jointly. It is slower because every `(query, document)` pair goes through the model, but it is usually better for reranking a candidate set.

`SparseEncoder` produces sparse vectors over vocabulary dimensions. It is used for SPLADE-style learned sparse retrieval, sparse vector indexes, interpretability via active tokens, and hybrid dense+sparse systems.

## Input Modalities

Text-only models accept strings. Multimodal models may accept:

- Image: PIL image, local file path, URL, numpy array, or torch tensor.
- Audio: local path, numpy array, torch tensor, dict with `array` and `sampling_rate`, or `torchcodec.AudioDecoder` when installed.
- Video: local path, numpy array, torch tensor, dict with `array` and `video_metadata`, or `torchcodec.VideoDecoder` when installed.
- Multimodal dicts: keys such as `text`, `image`, `audio`, `video`.
- Some vision-language models also accept chat-style message lists.

Check support with:

```python
print(model.modalities)
print(model.supports("image"))
print(model.supports(("text", "image")))  # CrossEncoder pair support
```

## Import Paths And Migration Notes

Top-level imports remain the preferred entry point:

```python
from sentence_transformers import SentenceTransformer, CrossEncoder, SparseEncoder
```

For v5.4+ internals, prefer model-type-specific packages:

```python
from sentence_transformers.sentence_transformer import losses, evaluation
from sentence_transformers.cross_encoder import losses as cross_losses
from sentence_transformers.sparse_encoder import losses as sparse_losses
from sentence_transformers.util.similarity import SimilarityFunction
from sentence_transformers.util.quantization import quantize_embeddings
```

Old paths for losses, evaluators, modules, and utilities may still work with deprecation warnings. Do not write new code against deprecated paths.

Important v5.4+ renames:

- `get_sentence_embedding_dimension()` -> `get_embedding_dimension()`
- `truncate_sentence_embeddings(dim)` -> `truncate_embeddings(dim)`
- `model.encode(sentences=...)` -> `model.encode(inputs=...)`
- `CrossEncoder.max_length` property -> `max_seq_length`
- trainer `tokenizer` argument -> `processing_class`
- `tokenizer_kwargs` -> `processor_kwargs`
- `CrossEncoder.forward()` returns a dict with `"scores"`.
- `push_to_hub(tags=...)` was removed; append tags to `model.model_card_data.tags` before pushing.

## Evidence Map Used To Create This Skill

| Evidence source | Why it matters | Skill use |
| --- | --- | --- |
| `pyproject.toml` | package name, dependencies, Python range, extras | install and verification guidance |
| `sentence_transformers/` | public classes, modules, source signatures | API references and migration guidance |
| `docs/quickstart.rst`, usage docs | intended examples and task routing | sub-skill workflows |
| `docs/package_reference/` | API families and trainer/evaluator docs | reference tables |
| `examples/` | semantic search, retrieve-rerank, sparse search, training recipes | scripts and practical workflows |
| `tests/` | behavior and import coverage | troubleshooting and safe smoke checks |
| `skills/train-sentence-transformers/` | existing production training guidance | training route and companion-skill note |
| installed package inspection | live signatures and imports | verified API signatures and runtime facts |
