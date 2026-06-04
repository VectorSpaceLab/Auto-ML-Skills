# Configuration Reference

Read this when adapting `flashrag-multimodal-pipeline-skill` to a concrete user request.

## What To Resolve

- Model, adapter, generator, retriever, or service path/name requested by the user.
- Data, corpus, dataset registry, prompt file, or prediction file required by the workflow.
- Output directory and log/summary paths.
- Smoke-test scale before full-scale execution.
- Optional dependencies or GPU/backend constraints.

## Practical Rule

Use the scripts bundled in `../scripts/` for deterministic validation, config generation, smoke execution, or output inspection when they fit the task. Use package CLIs/APIs for real execution. Avoid original repo example paths unless the user independently supplies a public checkout as their working project.
