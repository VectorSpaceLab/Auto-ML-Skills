# Troubleshooting

## Troubleshooting

- `Adapter is only valid for the LoRA method`: keep `finetuning_type: lora` when `adapter_name_or_path` is set.
- `Cannot merge adapters to a quantized model`: export from the unquantized base, then quantize the merged result in a second step.
- Missing adapter weights: run `validate_adapter.py`; use the checkpoint/final output directory that contains PEFT files.
- CPU export takes a long time: use `--export-device auto` with a free GPU and enough memory.
- Output still contains adapter files: you probably copied the adapter directory instead of running `llamafactory-cli export`; rerun and inspect `export.log`.
- Tokenizer save warning: inspect output; if tokenizer files are missing, check model path and `trust_remote_code`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-export-merge-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

