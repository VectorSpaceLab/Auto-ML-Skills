# Fully Async Rollout Workflow

Core args:

```bash
--rollout-function-path slime.rollout.fully_async_rollout.generate_rollout_fully_async
--sglang-server-concurrency 512
```

Use async runner:

```bash
python /path/to/skill/slime/scripts/run_slime_train_async.py ...
```

Custom hooks remain valid:

```bash
--custom-generate-function-path my_agent.generate
--custom-rm-path my_agent.reward
```

The fully async worker maintains a queue of in-flight generation groups and returns completed groups sorted by sample index within a rollout.

## Limitations

- No evaluation mode in the fully async rollout path.
- Ordering across rollouts is best-effort.
- Aborted groups can be requeued depending on data buffer behavior.
