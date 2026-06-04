# Troubleshooting

## Common Failures

- Retrieved docs lack `contents`: normalize retrieval output before tracing.
- Triple parser returns empty lists: inspect raw generated triple strings and the `<head; relation; tail>` pattern.
- Chain selection is unstable: reduce `num_choices`, `num_chains`, or `max_chain_length` for smoke tests.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-kg-trace-refiner-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

