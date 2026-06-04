---
name: llamafactory-api-client-tests-skill
description: "Use when a user wants LLaMA-Factory OpenAI-compatible client payload tests, tool calls, and image messages."
disable-model-invocation: true
---

# OpenAI-compatible client payload tests, tool calls, and image messages.

Use this sub-skill after the root `llama-factory` router selects `llamafactory-api-client-tests-skill`. It is focused on one workflow family and should be enough to validate inputs, generate/adapt configs, run a smoke test, inspect outputs, and then scale to the user's requested run without reopening the original repository docs.

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
- [scripts/make_payload.py](scripts/make_payload.py): bundled helper; run `python scripts/make_payload.py --help` before use.
- [scripts/run_client.py](scripts/run_client.py): bundled helper; run `python scripts/run_client.py --help` before use.
- [scripts/validate_payload.py](scripts/validate_payload.py): bundled helper; run `python scripts/validate_payload.py --help` before use.

## References

- [references/workflows.md](references/workflows.md): detailed end-to-end workflow distilled from the extracted skill.
- [references/cli-reference.md](references/cli-reference.md): configuration, data, CLI, or workflow details nearest to this sub-skill.
- [references/troubleshooting.md](references/troubleshooting.md): sub-skill-specific and general failure handling.

## Boundaries

This sub-skill does not own unrelated LLaMA-Factory capabilities. Return to the root router when the user asks for a different stage, backend, pipeline, service, or evaluation family.
