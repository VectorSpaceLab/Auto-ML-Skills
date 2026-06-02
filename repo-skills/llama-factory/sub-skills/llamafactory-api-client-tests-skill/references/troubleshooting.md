# Troubleshooting

## Common Failures

- Connection refused: start the LLaMA-Factory API server first.
- Tool calls are missing: the served model may not support function calling or the chat template may not expose tools.
- Image request rejected: use a VLM-compatible model and template; text-only chat models cannot consume image messages.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-api-client-tests-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

