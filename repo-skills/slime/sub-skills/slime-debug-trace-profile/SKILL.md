---
name: slime-debug-trace-profile
description: "Helps agents debug slime rollout and training separately, replay saved rollouts, inspect traces, profile SGLang rollout, and run CPU contract checks."
disable-model-invocation: true
---

# slime Debug Trace Profile

Use this sub-skill when the user reports a failure, wants to isolate rollout vs training, inspect a saved rollout, profile SGLang, or validate custom hook contracts before GPU jobs.

## Short Workflow

1. Reproduce with the smallest rollout/batch sizes.
2. Split rollout and training:
   - `--debug-rollout-only`
   - `--debug-train-only`
3. Save rollout dumps with `--save-debug-rollout-data`.
4. Replay with `--load-debug-rollout-data` or forge replay when engines should stay live.
5. For custom hooks, run CPU import/signature checks before Ray.
6. For performance, profile rollout workers through the SGLang router.

Read [references/workflows.md](references/workflows.md) for debug and profiling commands. Read [references/troubleshooting.md](references/troubleshooting.md) for common failure isolation patterns.

## Scripts

- Adapt [scripts/debug_args.sh](scripts/debug_args.sh) and [scripts/profile_rollout_request.py](scripts/profile_rollout_request.py).
- Use `slime-custom-rollout`'s hook validator for custom functions.
