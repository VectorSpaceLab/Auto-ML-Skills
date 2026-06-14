# Observability And Troubleshooting Workflow

## Report Bundle

Collect:

- `check_env.json`
- `inspect_api.json`
- `vllm collect-env` output when available
- server command and config
- server log
- request and response JSON
- `/health`, `/v1/models`, and `/metrics` snapshots
- benchmark JSON if performance-related

## Reduction

1. Reproduce with the smallest public model that exercises the same feature.
2. Remove LoRA, quantization, structured output, multimodal data, and distributed settings.
3. Add one feature back at a time.
4. Record the first feature that reintroduces failure.

## Resolution

After diagnosis, route to the owning sub-skill for the fix: serving config, LoRA, structured outputs, embeddings, multimodal, distributed, performance, or benchmarks.
