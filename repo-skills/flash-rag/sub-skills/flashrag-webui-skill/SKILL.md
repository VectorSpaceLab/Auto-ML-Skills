---
name: flashrag-webui-skill
description: "Use when a user wants FlashRAG WebUI launch, health check, and shutdown."
disable-model-invocation: true
---

# FlashRAG WebUI launch, health check, and shutdown.

Use this sub-skill after the root `flash-rag` router selects `flashrag-webui-skill`. It is focused on one workflow family and should be enough to validate inputs, generate/adapt configs, run a smoke test, inspect outputs, and then scale to the user's requested run without reopening the original repository docs.

## Short Workflow

1. Confirm the public package environment with the root script `../../scripts/check_flash_rag_env.py`.
2. Resolve user-provided model/data/corpus/output paths and choose smoke or full scale.
3. Read [references/workflows.md](references/workflows.md) for the detailed flow and placeholders to fill.
4. Read [references/cli-reference.md](references/cli-reference.md) for inputs, configs, and decision points.
5. Run or adapt the bundled helper scripts below; each script is inside this sub-skill directory.
6. Launch real work through installed FlashRAG package APIs or `python -m flashrag.retriever.index_builder` for index building; do not use private source checkout paths.
7. Inspect outputs, save logs/configs/summaries, and report `valid: true/false` with concrete artifact paths.

## Bundled Scripts

- [scripts/check_env.py](scripts/check_env.py): bundled helper; run `python scripts/check_env.py --help` before use.
- [scripts/check_webui.py](scripts/check_webui.py): bundled helper; run `python scripts/check_webui.py --help` before use.
- [scripts/run_webui.py](scripts/run_webui.py): bundled helper; run `python scripts/run_webui.py --help` before use.
- [scripts/stop_webui.py](scripts/stop_webui.py): bundled helper; run `python scripts/stop_webui.py --help` before use.

## References

- [references/workflows.md](references/workflows.md): detailed end-to-end workflow distilled from the extracted skill.
- [references/cli-reference.md](references/cli-reference.md): configuration, data, CLI, or workflow details nearest to this sub-skill.
- [references/troubleshooting.md](references/troubleshooting.md): sub-skill-specific and general failure handling.

## Boundaries

This sub-skill does not own unrelated FlashRAG capabilities. Return to the root router when the user asks for a different stage, backend, pipeline, service, or evaluation family.
