# Deployment Workflows

## Save A Local Model

```python
model.save_pretrained("models/my-model")
```

Saved model directories are self-contained when custom module classes are importable in the target environment. Standard models include `modules.json`, config files, tokenizer files, weights, and model card.

## Load Offline

```python
model = SentenceTransformer("models/my-model", local_files_only=True)
```

Use local paths and avoid network access in production startup when possible.

## Push To Hub

```python
url = model.push_to_hub("org-or-user/model-name", private=True)
```

For optimized artifacts on an upstream public model where you do not own the repo, use PR mode:

```python
export_optimized_onnx_model(
    model,
    optimization_config="O3",
    model_name_or_path="sentence-transformers/all-MiniLM-L6-v2",
    push_to_hub=True,
    create_pr=True,
)
```

Then load from the PR revision until merged:

```python
pull_request_number = 2
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    backend="onnx",
    revision=f"refs/pr/{pull_request_number}",
    model_kwargs={"file_name": "onnx/model_O3.onnx"},
)
```

## Select Optimized Files

Use `model_kwargs={"file_name": "..."}` to select a specific ONNX/OpenVINO artifact when multiple files exist.

## Serving Pattern

For embedding services:

1. Load the model once at process startup.
2. Batch requests where latency allows.
3. Normalize or quantize consistently with the index.
4. Return metadata that identifies model id, dimension, normalization, and precision.

For reranking services:

1. Limit candidate count per query.
2. Batch query-document pairs.
3. Keep score semantics documented: raw logits vs probabilities.

For sparse services:

1. Preserve sparse representation.
2. Track tokenizer/model version with the index.
3. Store document ids and payloads alongside sparse vectors.

## Reproducibility Checklist

Record:

- package version;
- model id or commit revision;
- backend and file name;
- embedding dimension or sparse vocabulary size;
- normalization setting;
- quantization/truncation settings;
- tokenizer/model revision;
- index build parameters.

## Security Notes

Do not enable `trust_remote_code=True` in production unless the model repository is trusted and pinned by revision.

Handle Hugging Face tokens through environment or secret management rather than hard-coding them in scripts.
