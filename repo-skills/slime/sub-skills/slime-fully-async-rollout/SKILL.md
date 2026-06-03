---
name: slime-fully-async-rollout
description: "Configures slime fully asynchronous rollout with train_async.py and generate_rollout_fully_async for long-tail generation workloads."
disable-model-invocation: true
---

# slime Fully Async Rollout

Use this sub-skill when rollout generation has long-tail latency and the user wants background in-flight generations across rollout boundaries.

## Short Workflow

1. Use root [../../scripts/run_slime_train_async.py](../../scripts/run_slime_train_async.py).
2. Do not set `--colocate`; async driver rejects colocation.
3. Set:
   ```bash
   --rollout-function-path slime.rollout.fully_async_rollout.generate_rollout_fully_async
   ```
4. Tune `--sglang-server-concurrency`.
5. Keep custom generate and reward hooks unchanged if already using them.

Read [references/workflows.md](references/workflows.md) for behavior and limitations. Read [references/troubleshooting.md](references/troubleshooting.md) for queue and eval caveats.

## Scripts

- Adapt [scripts/fully_async_args.sh](scripts/fully_async_args.sh).
