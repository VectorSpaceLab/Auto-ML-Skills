# Troubleshooting

## Common Failures

- Missing `fire`, `peft`, or `transformers`: install LLaMA-Factory dependencies in the environment.
- Target module not found: change `--target` to real linear module names or use a broader list known for the model.
- OOM or long CPU runtime: lower rank, use a smaller model for smoke, or do preflight only before scheduling a real run.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-adapter-init-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

