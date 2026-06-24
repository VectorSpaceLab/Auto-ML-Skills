# SFT Workflows

## Minimal SFT Args

```bash
SFT_ARGS=(
  --rollout-function-path slime.rollout.sft_rollout.generate_rollout
  --prompt-data /data/sft.jsonl
  --input-key messages
  --num-epoch 1
  --rollout-batch-size 8
  --global-batch-size 8
  --loss-type sft_loss
  --calculate-per-token-loss
  --disable-compute-advantages-and-returns
  --debug-train-only
)
```

Because `--debug-train-only` skips rollout serving paths, SFT can avoid launching SGLang engines when the data is already local and train-ready through the SFT rollout path.

## Checkpoint Args

```bash
CKPT_ARGS=(
  --hf-checkpoint /models/Qwen3-0.6B
  --ref-load /models/Qwen3-0.6B_torch_dist
  --load /runs/qwen3-0.6b-sft
  --save /runs/qwen3-0.6b-sft
  --save-interval 100
)
```

## Optimizer Args

SFT commonly uses higher LR than RL:

```bash
--optimizer adam
--lr 1e-5
--lr-decay-style cosine
--min-lr 1e-6
--lr-warmup-fraction 0.1
--weight-decay 0.1
```

## Async Driver

The public SFT examples use the async driver for prefetch:

```bash
python /path/to/skill/slime/scripts/run_slime_train_async.py ...
```

Do not combine this driver with `--colocate`.
