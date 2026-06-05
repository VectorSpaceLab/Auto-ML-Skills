---
name: vllm-serving-config
description: "Use when a user wants vLLM serving or engine configuration, YAML config files, tensor/pipeline/data parallel settings, dtype, max model length, quantization, memory, scheduler, or chat template arguments."
disable-model-invocation: true
---

# vLLM Serving Configuration

Use this sub-skill for selecting, validating, and explaining vLLM engine/server arguments for offline or online runs.

## Short Workflow

1. Gather model ID, hardware, GPU count, memory, context length, desired concurrency, quantization, and serve/offline mode.
2. Read [references/workflows.md](references/workflows.md) for configuration decision flow.
3. Read [references/engine-args.md](references/engine-args.md) for common args, YAML keys, and tradeoffs.
4. Generate a minimal config first, then validate it with bundled scripts before launching `vllm serve`.
5. Keep command-line overrides explicit because `vllm serve --config` uses command-line values over YAML values.

## Bundled Scripts

- [scripts/make_serve_config.py](scripts/make_serve_config.py): writes a minimal YAML serve config.
- [scripts/validate_config.py](scripts/validate_config.py): validates a config via the root validator.

## References

- [references/workflows.md](references/workflows.md): config creation, validation, and deployment path.
- [references/engine-args.md](references/engine-args.md): distilled engine/server arguments and pitfalls.

## Boundaries

Use `vllm-performance-tuning` for deeper KV cache/speculative/compile tuning, and `vllm-distributed-serving` for cluster or multi-node launch mechanics.
