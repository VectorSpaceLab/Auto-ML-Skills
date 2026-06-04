# Troubleshooting

## Common Failures

- Missing `trl`: install it; default model loader imports TRL value-head classes.
- `datasets>=2.16.0,<=4.0.0 is required`: install a compatible `datasets`, or add `--disable-version-check` for smoke-only validation.
- CUDA OOM on GPU 0: choose a free GPU with `nvidia-smi`, then rerun with `CUDA_VISIBLE_DEVICES=<id>`.
- Empty tokenized dataset: verify `dataset_info.json` maps `columns.prompt` to the text field.
- OOM: use LoRA, smaller `cutoff_len`, lower batch size, or QLoRA if bitsandbytes is available.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-pt-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

