# Low Precision Workflows

## BF16 Training With FP8 Rollout

Training checkpoint remains BF16 Megatron `torch_dist`:

```bash
--ref-load /models/model_bf16_torch_dist
```

SGLang rollout uses an FP8 HF checkpoint:

```bash
--hf-checkpoint /models/model_fp8_hf
```

Convert BF16 HF to FP8:

```bash
python /path/to/slime/tools/convert_hf_to_fp8.py \
  --model-dir /models/model_bf16_hf \
  --save-dir /models/model_fp8_hf \
  --strategy block \
  --block-size 128 128 \
  --max-workers 4
```

## FP8 KV Cache

```bash
--sglang-kv-cache-dtype fp8_e4m3
```

Use for long-context or multi-turn rollout when KV cache capacity is a bottleneck.

## FP8 Training

```bash
--fp8-format e4m3
--fp8-recipe blockwise
```

`--fp8-param-gather` can save memory but may conflict with CPU Adam offload paths.

## INT4 Rollout Or QAT

INT4 conversion requires calibration data:

```bash
python /path/to/slime/tools/convert_hf_to_int4.py \
  --input-dir /models/model_bf16_hf \
  --output-dir /models/model_int4_hf \
  --data-dir /data/calibration.jsonl \
  --num-calibration-samples 256 \
  --max-sequence-length 2048 \
  --trust-remote-code
```
