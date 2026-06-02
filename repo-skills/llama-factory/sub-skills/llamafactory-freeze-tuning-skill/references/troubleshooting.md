# Troubleshooting

## Common Failures

- `Current model does not support freeze tuning`: the model architecture lacks compatible layer naming; use LoRA or full tuning.
- No trainable parameters: lower `freeze_trainable_layers` or set `freeze_trainable_modules: all`.
- LLaMA-Pro divisibility error: the number of layers must be divisible by `freeze_trainable_layers` for that mode.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-freeze-tuning-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

