# Debug Troubleshooting

## Failure Before Ray Job Starts

Run root env check, then strict train check. Most pre-launch failures are environment or `PYTHONPATH`.

## Failure During Generation

Use rollout-only and save dump. Inspect:

- prompt lengths
- stop tokens
- reward outputs
- custom generate exceptions
- SGLang memory and health

## Failure During Train Step

Replay saved rollout with train-only. Inspect:

- `tokens` and `response_length`
- `loss_mask` length
- reward dtype
- global batch relation
- model recipe/checkpoint mismatch

## Profiling Adds Too Much Overhead

Start with short `--num-steps`, GPU-only activities, and no stack recording. Add CPU/stack/shape recording only when needed.
