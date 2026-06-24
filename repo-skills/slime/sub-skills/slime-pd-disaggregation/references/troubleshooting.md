# PD Troubleshooting

## `--sglang-config` And `--prefill-num-servers` Conflict

Use one path. Prefer YAML for new deployments.

## GPU Count Mismatch

Sum all group `num_gpus` values and match `--rollout-num-gpus`.

## Bad Throughput

Inspect whether prefill or decode is the bottleneck. Adjust number of prefill/decode engines and TP sizes. For multi-turn agents, also consider router session affinity.
