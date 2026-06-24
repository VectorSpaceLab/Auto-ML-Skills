# Fully Async Troubleshooting

## Colocation Assertion

Remove `--colocate` or use the synchronous runner.

## Queue Starvation

Increase `--sglang-server-concurrency`, reduce task timeout, or inspect whether external tools/reward services are bottlenecking.

## Need Evaluation

Use standard rollout for eval or run a separate evaluation workflow. Fully async rollout is training-oriented.
