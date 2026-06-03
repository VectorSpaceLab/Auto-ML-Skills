# `--sglang-config` Reference

Use `--sglang-config` for multi-model serving, PD disaggregation, heterogeneous server groups, and placeholder GPU reservations.

## Schema

```yaml
sglang:
  - name: actor
    model_path: /path/to/actor-or-default
    update_weights: true
    server_groups:
      - worker_type: regular
        num_gpus: 8
        num_gpus_per_engine: 4
        overrides:
          mem_fraction_static: 0.7
```

Model-level fields:

- `name`: unique model router name.
- `model_path`: optional, defaults to `--hf-checkpoint`.
- `update_weights`: whether training updates this model.
- `num_gpus_per_engine`: model-level TP override.
- `server_groups`: list of groups.

Server group fields:

- `worker_type`: `regular`, `prefill`, `decode`, or `placeholder`.
- `num_gpus`: total GPUs in the group.
- `num_gpus_per_engine`: group-level TP override.
- `overrides`: SGLang `ServerArgs` field names without `sglang_` prefix.

## Multi-Model Example

```yaml
sglang:
  - name: actor
    update_weights: true
    server_groups:
      - worker_type: regular
        num_gpus: 8
        num_gpus_per_engine: 4
  - name: ref
    model_path: /models/ref-hf
    update_weights: false
    server_groups:
      - worker_type: regular
        num_gpus: 4
        num_gpus_per_engine: 2
```

Custom rollout code can call `get_model_url(args, "ref")` from `slime.rollout.sglang_rollout`.

## Placeholder Group

```yaml
sglang:
  - name: actor
    server_groups:
      - worker_type: regular
        num_gpus: 4
      - worker_type: placeholder
        num_gpus: 4
```

Placeholders reserve GPU slots without starting engines.
