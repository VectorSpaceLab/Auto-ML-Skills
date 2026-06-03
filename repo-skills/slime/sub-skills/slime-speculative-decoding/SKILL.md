---
name: slime-speculative-decoding
description: "Configures slime speculative decoding, SGLang EAGLE flags, draft model paths, MTP checkpoint conversion, and online MTP training during RL."
disable-model-invocation: true
---

# slime Speculative Decoding

Use this sub-skill when the user asks to speed up rollouts with speculative decoding, EAGLE, draft models, MTP layers, or online MTP training.

## Short Workflow

1. Confirm the target model supports MTP/EAGLE or the user has a separate draft model.
2. Add SGLang speculative flags from [scripts/speculative_sglang_args.sh](scripts/speculative_sglang_args.sh).
3. If using a separate draft model, set `--sglang-speculative-draft-model-path`.
4. If training MTP layers online, ensure checkpoint conversion included `--mtp-num-layers`, then add [scripts/mtp_training_args.sh](scripts/mtp_training_args.sh).
5. Run a short rollout-only or tiny RL smoke test and compare throughput, accepted draft tokens, and generation correctness before scaling.

Read [references/configuration.md](references/configuration.md) for flag meanings and decision points. Read [references/troubleshooting.md](references/troubleshooting.md) for negative-speedup and checkpoint issues.

## Scripts

- [scripts/speculative_sglang_args.sh](scripts/speculative_sglang_args.sh): read or source this args block when enabling SGLang speculative decoding.
- [scripts/mtp_training_args.sh](scripts/mtp_training_args.sh): read or source this args block when enabling online MTP training.

## Related Sub-Skills

- `slime-sglang-deployment` for rollout engine topology and memory flags.
- `slime-checkpoint-conversion` for HF to torch-dist conversion with MTP weights.
- `slime-low-precision` when combining speculative decoding with FP8 or quantized rollout.
