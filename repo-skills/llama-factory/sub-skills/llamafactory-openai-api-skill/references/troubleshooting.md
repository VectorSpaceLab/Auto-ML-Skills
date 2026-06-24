# Troubleshooting

## Troubleshooting

- `fastapi`/`uvicorn`/`sse_starlette` import errors: install the API dependencies in the same environment.
- Connection refused: wait for model loading, inspect the log, and ensure the selected port is free.
- 401 unauthorized: pass `Authorization: Bearer <API_KEY>`; `check_api.py --api-key` does this.
- Empty or `<think>`-prefixed output: this is model behavior, not API failure. Use a stricter system prompt, lower `max_tokens`, or postprocess reasoning tags.
- CUDA OOM on startup: choose a free GPU, lower dtype/memory settings, or serve a merged smaller model.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-openai-api-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

