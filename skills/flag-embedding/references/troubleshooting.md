# Troubleshooting

Read this for cross-cutting FlagEmbedding install, import, model loading, device, and workflow failures.

## Install And Import

Check the package first:

```bash
python -m pip check
python - <<'PY'
import importlib.metadata as md
import FlagEmbedding
print(md.version("FlagEmbedding"))
print(FlagEmbedding.__file__)
PY
```

If import fails:

- Confirm `torch`, `transformers`, `datasets`, `accelerate`, `sentence_transformers`, `peft`, `ir-datasets`, `sentencepiece`, and `protobuf` are installed in the same Python environment.
- Run `python scripts/check_flagembedding_env.py --show-torch` from this skill to inspect imports and torch backend visibility without downloading models.
- Avoid Python versions unsupported by the current torch/transformers wheels. For ML environments, Python 3.10 or 3.11 is usually safer than a newer unreleased wheel path.

## Model Loading

`FlagAutoModel.from_finetuned()` and `FlagAutoReranker.from_finetuned()` infer the class from the basename of `model_name_or_path`. If a local checkpoint directory is named `checkpoint-123`, the auto loader uses the parent directory basename.

When auto loading raises "Model name ... not found in the model mapping":

1. Choose the correct explicit `model_class` from `references/model-overview.md`.
2. Pass matching defaults such as `pooling_method`, `trust_remote_code`, and instruction format.
3. Use the concrete class directly if needed, for example `FlagModel`, `BGEM3FlagModel`, `FlagLLMModel`, `FlagReranker`, or `LayerWiseFlagLLMReranker`.

For Hugging Face models that require custom code, pass `trust_remote_code=True` only after the user accepts that remote model code will execute.

## Device And Precision

If a model unexpectedly uses all GPUs, pass an explicit device list:

```python
model = FlagAutoModel.from_finetuned("BAAI/bge-base-en-v1.5", devices=["cuda:0"])
```

If CUDA is not available in torch:

- Verify `python -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"`.
- Confirm the installed torch wheel matches the host driver and GPU architecture.
- Use `devices="cpu"` and `use_fp16=False` for CPU-only diagnosis.

If CPU inference fails with half-precision operations, set `use_fp16=False`. If GPU inference produces unsupported dtype issues, try `use_fp16=False` or `use_bf16=True` only for model families that support it.

## Output Shapes And Types

Normal embedders return a one-dimensional vector for a single string and a two-dimensional array for a list of strings when `convert_to_numpy=True`.

`BGEM3FlagModel.encode()` returns a dictionary when sparse or ColBERT modes are requested. Common keys are:

- `dense_vecs`
- `lexical_weights`
- `colbert_vecs`

Rerankers return raw scores by default. Pass `normalize=True` to map reranker scores through sigmoid where the reranker implementation supports it.

## Fine-Tuning Failures

Before launching `torchrun`, validate training data with `sub-skills/finetuning/scripts/validate_finetune_jsonl.py`.

Common data failures:

- Missing `query`, `pos`, or `neg`.
- `pos` or `neg` is not a list of strings.
- `pos_scores` or `neg_scores` length does not match `pos` or `neg` when knowledge distillation is enabled.
- `train_data` paths do not exist; the argument dataclasses raise `FileNotFoundError`.

Common environment failures:

- `flash-attn` build errors: install only when a decoder-only or training workflow needs flash attention, and match torch/CUDA/compiler versions.
- `deepspeed` errors: confirm CUDA, compiler, torch, and the selected deepspeed config are compatible.
- Out-of-memory: reduce per-device batch size, use gradient accumulation, shorten max lengths, lower train group size, disable cross-device negatives, or move to a smaller model.

## Evaluation Failures

Before running a custom evaluation, validate dataset layout with `sub-skills/evaluation/scripts/validate_custom_eval_dataset.py`.

Common benchmark dependency gaps:

- MTEB examples require `mteb`.
- BEIR examples require `beir`.
- AIR-Bench examples require `air-benchmark`.
- Many retrieval metrics need `pytrec_eval`; when installation fails, try `pytrec-eval-terrier`.
- FAISS install differs by Python, CUDA, and platform. Choose CPU or GPU wheels deliberately.

If evaluation silently reuses old results, check `--overwrite`. If corpus embeddings are expensive, use `--corpus_embd_save_dir` deliberately and document cache reuse.
