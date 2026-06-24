# Model Recipe Troubleshooting

## Shape Mismatch During Conversion Or Load

The recipe does not match the HF checkpoint. Check hidden size, layer count, GQA groups, vocab size, MoE expert counts, and plugin `--spec`.

## Training Runs But Text Is Garbled

The checkpoint may load but use a wrong tokenizer/config pairing, RoPE base, or model plugin. Confirm:

- `--hf-checkpoint` points at the architecture-compatible HF checkpoint.
- `--ref-load` was converted with the same recipe.
- `--model-name` is set if transformer config auto-detection races or fails on shared filesystems.

## Attention Backend Errors

For some architectures or hardware, `--attention-backend flash` may need to be changed or removed. VLM and AMD paths have separate sub-skills.
