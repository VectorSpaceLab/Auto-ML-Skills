# Rollout Correction Troubleshooting

## No Rollout Logprobs

Correction methods that compare rollout and training policies need rollout logprobs. Ensure the custom generate path requests and preserves logprobs.

## High Variance Or Training Collapse

Start with metrics only. Then try clipping/truncation. Sequence-level importance weights can have high variance; token/geometric levels are often more stable.

## Mismatch From Retokenization

Agentic workflows must preserve sampled token IDs. Retokenizing final text invalidates rollout logprobs.
