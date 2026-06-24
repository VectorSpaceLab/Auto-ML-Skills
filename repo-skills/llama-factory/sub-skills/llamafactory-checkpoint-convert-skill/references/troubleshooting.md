# Troubleshooting

## Common Failures

- DCP conversion loads the whole model on CPU; ensure enough RAM and disk.
- `dcp2hf` requires a config path from the original HF model.
- Conversion scripts may not copy tokenizers; inspect the output and copy tokenizer files from the source model if needed.
- Pass-through scripts differ by model family; keep the generated `command.json` so failures are reproducible.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-checkpoint-convert-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

