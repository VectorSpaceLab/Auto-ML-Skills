# Troubleshooting

## Troubleshooting

- `split not loaded`: check that the split file is at `data_dir/dataset_name/<split>.jsonl`, not directly under `data_dir`.
- Output dir not where expected: FlashRAG appends `<dataset>_<timestamp>_<save_note>` when `disable_save: false`.
- `tiktoken` import error while using fake components: `flashrag.prompt` imports `tiktoken` at module import time; install it even when no OpenAI API call is made.
- `termcolor` import error from `flashrag.pipeline`: use this skill's runner or install `termcolor`; package-level pipeline imports pull in reasoning pipeline extras.
- Real generator loads a remote model unexpectedly: set `generator_model_path` to a local model path and use the correct `framework`.
- Refiner model loads unexpectedly: keep `refiner_name: null` for baseline sequential runs.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-sequential-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

