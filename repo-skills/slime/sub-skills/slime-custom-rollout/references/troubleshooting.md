# Custom Rollout Troubleshooting

## Wrong Container Shape

Most training paths expect `list[list[Sample]]`, grouped by prompt. Do not flatten groups unless the target hook explicitly expects flattened samples.

## Missing Required Sample Fields

Training samples should have:

- `tokens`
- `response_length`
- `reward`
- `status`

Set `loss_mask` when only part of the response should train.

## Reward Dicts Not Selected

If rewards are dictionaries, configure:

```bash
--reward-key <key>
--eval-reward-key <key>
```

## Blocking Network Calls

Reward and generate hooks are async-capable. Use async HTTP clients or bounded concurrency for remote services.
