# Cross-cutting Troubleshooting

Use this reference for failures that affect more than one FlagEmbedding workflow. Workflow-specific issues live in the nearest sub-skill troubleshooting file.

## Import or Dependency Failures

### `ModuleNotFoundError: No module named 'torch'` or `transformers`

Likely cause: FlagEmbedding imports depend on Torch and Transformers even when you only inspect APIs.

Recovery:

1. Install the base package with runtime dependencies: `pip install -U FlagEmbedding`.
2. For local source work, use `pip install -e .` from the checkout plus the dependencies from package metadata.
3. Run `python scripts/check_install.py --json` from this skill directory to confirm imports and Torch backend visibility.

### Fine-tune extra missing `deepspeed` or `flash_attn`

Likely cause: training commands use optional accelerator packages not needed for inference.

Recovery:

- Install `FlagEmbedding[finetune]` only when constructing an environment that will actually run training.
- Match `flash-attn` and DeepSpeed versions to the installed Torch/CUDA stack.
- If the user only needs data validation or command construction, use the `finetuning` bundled scripts without installing the extra.

## Hardware and Precision Failures

### FP16/BF16 on CPU or unsupported accelerator

Symptoms include dtype errors, slow CPU inference, or model load failures after setting `use_fp16=True` or `use_bf16=True`.

Recovery:

- For CPU-only diagnostics, set `use_fp16=False` and `use_bf16=False`.
- Use explicit `devices='cpu'` when avoiding GPU auto-selection.
- For CUDA, verify `torch.cuda.is_available()` and driver compatibility before using GPU devices.

### Device auto-selection surprises

FlagEmbedding base classes choose CUDA first when available, then NPU, MUSA, MPS, and finally CPU. Integer `devices` values are interpreted as CUDA or MUSA device indices.

Recovery:

- Pass devices explicitly, such as `devices='cpu'`, `devices=['cuda:0']`, or `devices=['cuda:0', 'cuda:1']`.
- Avoid integer devices unless CUDA/MUSA is intended.

## Model Download and Cache Failures

Symptoms include Hugging Face timeout errors, authentication failures, missing local files, or `trust_remote_code` warnings.

Recovery:

1. Decide whether the model is public, private, or local.
2. For private models, authenticate outside the generated skill and avoid writing tokens into code or logs.
3. For local checkpoints, verify that tokenizer/config/model files exist.
4. If the checkpoint name is not in FlagEmbedding's auto mapping, route to `sub-skills/model-catalog-and-rag/` to choose an explicit `model_class`, then route to `sub-skills/inference/` for code.

## Version Compatibility

- FlagEmbedding `1.4.0` declares `transformers>=4.44.2,<6.0.0` in source metadata.
- Tests include a compatibility check for Transformers 5 behavior around `is_torch_fx_available`.
- If an environment has incompatible Transformers/Torch versions, prefer creating a clean environment over patching a shared one.

## Safe Verification Order

1. Run the root import check.
2. Run `scripts/check_install.py --json`.
3. For inference, run sub-skill script help/snippet generation before loading a model.
4. For fine-tuning, validate JSONL and build a command before running distributed training.
5. For evaluation, generate a command plan and confirm dataset/cache availability before running benchmarks.
