---
name: llamafactory-inference-skill
description: "Use when a user wants LLaMA-Factory Offline chat, one-shot inference, batch prediction, and adapter inference."
disable-model-invocation: true
---

# Offline chat, one-shot inference, batch prediction, and adapter inference.

Use this sub-skill after the root `llama-factory` router selects `llamafactory-inference-skill`. It is focused on one workflow family and should be enough to validate inputs, generate/adapt configs, run a smoke test, inspect outputs, and then scale to the user's requested run without reopening the original repository docs.

## Short Workflow

1. Confirm the public package environment with the root script `../../scripts/check_llama_factory_env.py`.
2. Resolve user-provided model/data/corpus/output paths and choose smoke or full scale.
3. Read [references/workflows.md](references/workflows.md) for the detailed flow and placeholders to fill.
4. Read [references/cli-reference.md](references/cli-reference.md) for inputs, configs, and decision points.
5. Run or adapt the bundled helper scripts below; each script is inside this sub-skill directory.
6. Launch real work through `llamafactory-cli` or verified package APIs, not through a private source checkout.
7. Inspect outputs, save logs/configs/summaries, and report `valid: true/false` with concrete artifact paths.

## Bundled Scripts

- [scripts/check_env.py](scripts/check_env.py): bundled helper; run `python scripts/check_env.py --help` before use.
- [scripts/common.py](scripts/common.py): support module imported by nearby scripts; read or adapt it only when modifying helper behavior.
- [scripts/inspect_inference.py](scripts/inspect_inference.py): bundled helper; run `python scripts/inspect_inference.py --help` before use.
- [scripts/make_chat_config.py](scripts/make_chat_config.py): bundled helper; run `python scripts/make_chat_config.py --help` before use.
- [scripts/make_predict_config.py](scripts/make_predict_config.py): bundled helper; run `python scripts/make_predict_config.py --help` before use.
- [scripts/run_chat_once.py](scripts/run_chat_once.py): bundled helper; run `python scripts/run_chat_once.py --help` before use.
- [scripts/run_predict.py](scripts/run_predict.py): bundled helper; run `python scripts/run_predict.py --help` before use.

## References

- [references/workflows.md](references/workflows.md): detailed end-to-end workflow distilled from the extracted skill.
- [references/cli-reference.md](references/cli-reference.md): configuration, data, CLI, or workflow details nearest to this sub-skill.
- [references/troubleshooting.md](references/troubleshooting.md): sub-skill-specific and general failure handling.

## Boundaries

This sub-skill does not own unrelated LLaMA-Factory capabilities. Return to the root router when the user asks for a different stage, backend, pipeline, service, or evaluation family.
