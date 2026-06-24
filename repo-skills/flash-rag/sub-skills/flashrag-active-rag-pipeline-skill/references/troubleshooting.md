# Troubleshooting

## Common Failures

- `return_scores` unsupported: use a generator backend that exposes scores/logprobs or switch to SelfAsk/IRCOT.
- Infinite-looking loops: reduce `max_iter`, `max_generation_length`, and `test_sample_num`.
- Bad final parsing: inspect per-iteration outputs in `intermediate_data.json`.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-active-rag-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

