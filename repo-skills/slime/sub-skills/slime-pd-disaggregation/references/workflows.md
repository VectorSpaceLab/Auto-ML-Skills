# PD Disaggregation Workflows

## Simple Legacy Path

```bash
--prefill-num-servers 1
--rollout-num-gpus 16
--rollout-num-gpus-per-engine 8
```

This creates prefill/decode separation for one model. It is simple but less flexible than YAML.

## YAML Path

```yaml
sglang:
  - name: actor
    update_weights: true
    server_groups:
      - worker_type: prefill
        num_gpus: 8
        num_gpus_per_engine: 4
      - worker_type: decode
        num_gpus: 8
        num_gpus_per_engine: 4
```

Launch with:

```bash
--sglang-config sglang_pd.yaml
--rollout-num-gpus 16
```

## When To Use

PD is useful when prefill and decode have different bottlenecks, especially long-context, multi-turn, or agentic workloads where prompt growth dominates.
