# Low Precision Troubleshooting

## Quantized Rollout Generates Bad Text

Run rollout-only debug on a tiny prompt before training:

```bash
--debug-rollout-only
--save-debug-rollout-data /tmp/rollout_{rollout_id}.pt
```

Check stop tokens and tokenization before blaming quantization.

## SGLang Illegal Memory Access

Treat as possible OOM. Lower `--sglang-mem-fraction-static` and reduce context length.

## FP8 Param Gather Conflict

If using CPU Adam offload, avoid `--fp8-param-gather` unless the optimizer path supports it.

## HF Export Compatibility

Quantized HF export can be sensitive to `transformers` and `modelopt` versions. Test import and one generation after export.
