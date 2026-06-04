# Troubleshooting

## Troubleshooting

- `No module named bitsandbytes`: install bitsandbytes or use a non-bnb method supported by the environment.
- CUDA kernel errors: verify the installed bitsandbytes wheel matches CUDA.
- LoRA/torchao compatibility errors: pin `peft<=0.18.1` or remove/upgrade incompatible `torchao`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-qlora-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

