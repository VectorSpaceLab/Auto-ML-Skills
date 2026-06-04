# Troubleshooting

## Common Failures

- Missing PEFT feature: pin or upgrade `peft` to a version supporting the requested variant.
- PiSSA with PPO/KTO/ref model: unsupported; use SFT or compatible stages.
- DoRA/rsLoRA on unsupported target modules: reduce `lora_target` to known linear module names or use `all`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-adapter-variants-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

