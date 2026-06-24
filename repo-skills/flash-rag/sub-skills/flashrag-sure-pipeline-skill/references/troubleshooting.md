# Troubleshooting

## Troubleshooting

- `No valid predictions!`: generator output did not match the `(a) ... (b) ...` candidate format.
- `ranking_scores` missing: pairwise ranking prompts did not run; check whether candidate count is at least 2.
- Optional import errors from `flashrag.pipeline`: use this skill's runner; package-level pipeline imports pull in unrelated advanced pipelines.
- Scores are poor with real models: inspect `candidates`, `val_scores`, and `ranking_scores` in `intermediate_data.json` before changing retriever settings.
- Stub limitations: the bundled stubs are only for this fake smoke path. Do not use them for dense retrieval, real generator inference, tokenizer-dependent truncation, or model-based metrics.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-sure-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

