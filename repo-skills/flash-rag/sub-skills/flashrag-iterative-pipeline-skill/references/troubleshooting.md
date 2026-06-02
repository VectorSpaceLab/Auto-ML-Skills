# Troubleshooting

## Troubleshooting

- `split not loaded`: the split must be under `data_dir/dataset_name/<split>.jsonl`.
- Missing iteration fields in `intermediate_data.json`: ensure `--iter-num` used for inspect matches the config/run value.
- Optional import errors from `flashrag.pipeline`: use this skill's runner; package-level pipeline imports pull in unrelated advanced pipelines.
- Real generator loads a remote model unexpectedly: set `generator_model_path` to a local model path and choose the correct `framework`.
- Stub limitations: the bundled stubs are only for this fake smoke path. Do not use them for dense retrieval, real generator inference, tokenizer-dependent truncation, or model-based metrics.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-iterative-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

