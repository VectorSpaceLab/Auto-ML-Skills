# SentenceTransformer Troubleshooting

## Similarity Scores Are Poor

Check task shape first:

- Symmetric search: query and corpus entries have similar structure and length.
- Asymmetric search: short query searches longer passages or documents.

Use a model trained for the matching task. For asymmetric retrieval, use `encode_query` and `encode_document`.

If dot product search behaves badly, ensure embeddings are normalized when you expect cosine-like behavior:

```python
embeddings = model.encode(texts, normalize_embeddings=True)
```

## Query And Document Prompts Are Ignored

Use `encode_query` and `encode_document`, not plain `encode`, unless you intentionally pass `prompt` or `prompt_name`.

Inspect prompts:

```python
print(model.prompts)
print(model.default_prompt_name)
```

For custom models with `Router`, confirm that the query/document task maps to the intended route.

## Multimodal Inputs Fail

Install the relevant extra:

```bash
pip install -U "sentence-transformers[image]"
pip install -U "sentence-transformers[audio]"
pip install -U "sentence-transformers[video]"
```

Then verify model support:

```python
print(model.modalities)
print(model.supports("image"))
```

A model that only supports text cannot encode images just because the image extra is installed.

## Shape Or Return Type Surprises

Default `encode` returns a NumPy array for sentence embeddings. Set `convert_to_tensor=True` for torch tensors.

For a single string input, some downstream code may expect a batch dimension. Wrap the input in a list when you need a 2D array:

```python
embedding = model.encode(["one sentence"])
```

`output_value="token_embeddings"` returns token-level outputs and is not a drop-in replacement for sentence embeddings.

## Exact Search Is Slow

`semantic_search` is exact chunked search. It is convenient but not the final architecture for million-scale corpora.

For large corpora, precompute embeddings and use a vector index. Tune ANN recall/speed parameters before blaming the embedding model.

## Memory Problems

Reduce `batch_size`, lower `corpus_chunk_size`, use CPU for large corpus tensors if GPU memory is too small, or quantize/truncate embeddings.

For multi-device offline jobs, use `start_multi_process_pool` and `encode_multi_process`, but keep ordinary `encode` for simple online requests.

## Local Or Offline Loading

Use a local model directory plus `local_files_only=True`. If the local directory is a saved Sentence Transformer, it should contain `modules.json` and `config_sentence_transformers.json`.
