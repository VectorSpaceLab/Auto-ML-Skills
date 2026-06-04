# Troubleshooting

## Common Failures

- No query extracted: check whether the model emits the exact begin/end query tags.
- All samples hit max retrieval: lower task complexity or improve prompt/examples.
- Final answer is blank: inspect whether the model ended with the configured answer tag or boxed pattern.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-reasoning-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

