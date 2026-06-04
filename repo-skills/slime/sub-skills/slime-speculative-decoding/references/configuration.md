# Speculative Decoding Configuration

Read this when enabling speculative decoding for slime rollouts.

## SGLang EAGLE Flags

Typical MTP/EAGLE setup:

```bash
--sglang-speculative-algorithm EAGLE
--sglang-speculative-num-steps 3
--sglang-speculative-eagle-topk 1
--sglang-speculative-num-draft-tokens 4
```

If using a separately trained draft model:

```bash
--sglang-speculative-draft-model-path <draft_model_path>
```

These are SGLang server flags passed through slime by prefixing with `--sglang-`.

## Online MTP Training

Online MTP training keeps the draft distribution closer to the target policy during RL:

```bash
--mtp-num-layers 1
--enable-mtp-training
--mtp-loss-scaling-factor 0.2
```

Checkpoint conversion must include the same MTP layer count so the torch-dist checkpoint contains the relevant weights.

## When To Use

- Use speculative decoding when rollout decoding latency is a bottleneck and acceptance remains high.
- Use online MTP when acceptance degrades during RL because target and draft distributions drift.
- Avoid adding this to an unstable baseline; first prove normal rollout training works.

## Validation Signals

- SGLang server starts with speculative config accepted.
- Throughput improves on representative prompts.
- Acceptance metrics or generated-token timing show positive speedup.
- Reward/loss behavior remains close to the non-speculative baseline on a tiny run.
