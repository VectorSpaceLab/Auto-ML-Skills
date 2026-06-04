# Rollout Correction Configuration

## Metrics Only

```bash
--get-mismatch-metrics
```

This monitors rollout-training policy mismatch without changing loss.

## Use Rollout Logprobs

```bash
--use-rollout-logprobs
```

This can skip recomputing old logprobs in selected workflows.

## TIS

```bash
--use-tis
--tis-clip 2.0
--tis-clip-low 0.0
```

Custom implementation:

```bash
--custom-config-path mis.yaml
--custom-tis-function-path my_project.mis.compute_mis_weights_with_cp
```

## Related Advanced Flags

```bash
--use-routing-replay
--use-rollout-routing-replay
--use-opsm
--opsm-delta 1e-4
```

Use these for specific MoE/off-policy stability experiments only after baseline metrics are understood.
