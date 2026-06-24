# Troubleshooting

## Common Failures

- Method checkpoint missing: keep fake smoke output and report required `model_path` or `generator_model_path`.
- Dataset name not present under `data_dir`: create a FlashRAG dataset split first.
- Refiner dependencies missing, such as spaCy or LLMLingua: preflight should warn before real execution.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-methods-runner-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

