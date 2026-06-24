# Conversion CLI Reference

## Bundled `scripts/convert_hf_to_torch_dist.py`

Important flags:

- `--hf-checkpoint`: local Hugging Face model directory.
- `--save`: output Megatron checkpoint directory.
- Megatron model architecture args: `--num-layers`, `--hidden-size`, `--num-attention-heads`, model plugin `--spec`, and related flags.
- `--megatron-to-hf-mode`: `raw` or `bridge`.
- `--padded-vocab-size`: optional override.

## Bundled `scripts/convert_torch_dist_to_hf.py`

Important flags:

- `--input-dir`: Megatron iteration directory such as `iter_0000100`.
- `--output-dir`: Hugging Face output directory.
- `--origin-hf-dir`: original HF checkpoint for config/tokenizer and parameter naming.
- `--model-name`: alternative to origin HF dir for naming.
- `--force`: overwrite existing output.
- `--add-missing-from-origin-hf`: copy missing weights from the original HF checkpoint.
- `--chunk-size`: export chunk size.
- `--vocab-size`: override when Megatron padded vocab affects embeddings.

## FP8 And INT4 Tools

For FP8/INT4, route to `slime-low-precision`. Basic tool names:

- `convert_hf_to_fp8.py`
- `convert_hf_to_int4.py`
- `convert_hf_to_int4_direct.py`

These are heavy conversion paths and may require modelopt, quantization datasets, CUDA, and enough CPU/GPU memory.
