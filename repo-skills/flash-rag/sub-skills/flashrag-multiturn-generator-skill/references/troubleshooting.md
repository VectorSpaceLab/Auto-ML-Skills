# Troubleshooting

## Common Failures

- Two adjacent user messages: insert an assistant/system message or split into separate runs.
- Empty second turn: validate messages before rendering.
- Model path missing: run fake smoke and report the missing path before scheduling a real run.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-multiturn-generator-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

