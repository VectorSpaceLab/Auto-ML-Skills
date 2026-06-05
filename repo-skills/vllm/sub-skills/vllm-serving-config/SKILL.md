---
name: vllm-serving-config
description: "Use when a user wants vLLM serving or engine configuration, YAML config files, tensor/pipeline/data parallel settings, dtype, max model length, quantization, memory, scheduler, or chat template arguments."
disable-model-invocation: true
---

# vLLM Serving Configuration

Use this sub-skill for selecting, validating, and explaining vLLM engine/server arguments for offline or online runs. It owns base configuration before the user moves to serving, offline inference, performance tuning, or distributed deployment.

## Use When

- The user wants a `vllm serve` command, YAML config, or engine argument set.
- The user asks about dtype, max model length, memory utilization, quantization, tokenizer, chat template, scheduler, parallelism, or config-file precedence.
- The user needs to validate a config before launching a server or batch job.
- The user has an OOM or bad-argument failure that likely comes from engine args.

## Inputs To Collect

- Model ID, hardware, GPU count, memory, desired context length, concurrency, dtype, quantization, tokenizer path, and endpoint mode.
- Whether the output should be a CLI command, YAML file, Python kwargs, or an explanation of tradeoffs.
- Existing config/command and exact error if validation is for a failed run.

## Short Workflow

1. Gather model ID, hardware, GPU count, memory, context length, desired concurrency, quantization, and serve/offline mode.
2. Read [references/workflows.md](references/workflows.md) for configuration decision flow.
3. Read [references/engine-args.md](references/engine-args.md) for common args, YAML keys, and tradeoffs.
4. Generate a minimal config first, then validate it with bundled scripts before launching `vllm serve`.
5. Keep command-line overrides explicit because `vllm serve --config` uses command-line values over YAML values.
6. Route specialized flags to the relevant sub-skill instead of hiding complex behavior in a generic config.

## Bundled Scripts

- [scripts/make_serve_config.py](scripts/make_serve_config.py): writes a minimal YAML serve config.
- [scripts/validate_config.py](scripts/validate_config.py): validates a config via the root validator.

## References

- [references/workflows.md](references/workflows.md): config creation, validation, and deployment path.
- [references/engine-args.md](references/engine-args.md): distilled engine/server arguments and pitfalls.

## Boundaries

Use `vllm-performance-tuning` for deeper KV cache/speculative/compile tuning, and `vllm-distributed-serving` for cluster or multi-node launch mechanics.

## Verification Notes

- The validators catch structure and common value mistakes, not full model compatibility.
- A config is runtime-validated only after `vllm serve` or offline `LLM(...)` loads the model and completes a request.
- Keep public examples on public model IDs or placeholders.
